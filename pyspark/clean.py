from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, lit, avg, posexplode, count
from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType, ArrayType, IntegerType, StringType
import requests

def filter_and_drop_rows(df):
    # remove invalid respondents and check compensation is not NA
    filtered_df = df.filter(
        (df.Check == "Apples")&
        (df.MainBranch == "I am a developer by profession")&
        ((df.Employment == "Employed, full-time") | 
         (df.Employment == "Employed, part-time") |
         (df.Employment == "Independent contractor, freelancer, or self-employed"))&
        (df.CompTotal != "NA"))

    dropped_df = filtered_df.drop(
        "ResponseId","MainBranch","Check","CodingActivities","LearnCodeOnline","TechDoc","PurchaseInfluence","BuyNewTool","BuildvsBuy","TechEndorse",
        "LanguageWantToWorkWith","LanguageAdmired","DatabaseWantToWorkWith","DatabaseAdmired","PlatformWantToWorkWith", "PlatformAdmired",
        "WebframeWantToWorkWith","WebframeAdmired","EmbeddedWantToWorkWith","EmbeddedAdmired","MiscTechWantToWorkWith", "MiscTechAdmired",
        "ToolsTechWantToWorkWith","ToolsTechAdmired","NEWCollabToolsWantToWorkWith","NEWCollabToolsAdmired", "OpSysPersonal use","OfficeStackAsyncHaveWorkedWith", 
        "OfficeStackAsyncWantToWorkWith","OfficeStackAsyncAdmired", "OfficeStackSyncHaveWorkedWith", "OfficeStackSyncWantToWorkWith","OfficeStackSyncAdmired",
        "AISearchDevWantToWorkWith","AISearchDevAdmired","NEWSOSites","SOVisitFreq","SOAccount","SOPartFreq","SOHow","SOComm","AIBen",
        "AINextMuch more integrated", "AINextNo change","AINextMore integrated","AINextLess integrated","AINextMuch less integrated","AIEthics",
        "AIChallenges","TBranch","Knowledge_1","Knowledge_2","Knowledge_3","Knowledge_4","Knowledge_5","Knowledge_6","Knowledge_7","Knowledge_8",
        "Knowledge_9","Frequency_1","Frequency_2","Frequency_3","TimeSearching","TimeAnswering","Frustration","ProfessionalTech","ProfessionalCloud",
        "ProfessionalQuestion","JobSatPoints_1","JobSatPoints_4","JobSatPoints_5","JobSatPoints_6","JobSatPoints_7","JobSatPoints_8",
        "JobSatPoints_9","JobSatPoints_10","JobSatPoints_11","SurveyLength","SurveyEase","ConvertedCompYearly","JobSat", 
    )
    return dropped_df

def clean_data(df):
    URL = "https://openexchangerates.org/api/latest.json"
    params = {"app_id": "a82429fa6fdb42f8855e6efc1d92e60c"}
    conversion_rates = requests.get(URL, params=params).json()["rates"]

    def convert_to_USD(currency, amount):
        if not currency or not amount:
            return None
        currency = currency.split()[0]
        if currency not in conversion_rates:
            return None
        if 'e' in amount or '.' in amount:
            integer_amount = int(float(amount))
        else:
            integer_amount = int(amount)
        return round(int(integer_amount)/conversion_rates[currency], 2)
    convert_to_usd_udf = udf(convert_to_USD, FloatType())

    cleaned_df = (
        df
        .withColumn("CompTotal(USD)", 
                    when( ((col("Currency").isNull()) | 
                            (col("Currency") == "NA") |
                            (col("CompTotal") == "None") |
                           (col("CompTotal").isNull())), lit(None))
                    .otherwise(convert_to_usd_udf(col("Currency"), col("CompTotal"))))
        .withColumn("YearsCode", 
                    when( ((col("YearsCode")=="NA") | (col("YearsCode").isNull())), lit(None))
                    .otherwise(col("YearsCode").cast(IntegerType())))
        .withColumn("WorkExp",
                    when( ((col("WorkExp")=="NA") | (col("WorkExp").isNull())), lit(None))
                    .otherwise(col("WorkExp").cast(IntegerType())))
        .withColumnRenamed("NEWCollabToolsHaveWorkedWith", "CollabToolsHaveWorkedWith")
        .withColumnRenamed("OpSysProfessional use", "OpSysProfessionalUse")
        .withColumnRenamed("AIToolCurrently Using", "AIToolCurrentlyUsing")
        .withColumnRenamed("AIToolInterested in Using", "AIToolInterestedUsing")
        .withColumnRenamed("AIToolNot interested in Using", "AIToolNotInterestedUsing")
        .withColumnRenamed("PlatformHaveWorkedWith", "CloudHaveWorkedWith")
        .withColumnRenamed("ToolsTechHaveWorkedWith", "DevToolHaveWorkedWith")
    )
    # filtering after transformation
    cleaned_df = cleaned_df.filter(
        ~((col("CompTotal(USD)").isNull())|(col("CompTotal(USD)") == float("inf"))|(col("CompTotal(USD)") > float("1E6")))
    )
    return cleaned_df

def to_postgres(df, table_name: str):
    df.write.format("jdbc")\
        .mode("overwrite")\
        .option("url", "jdbc:postgresql://localhost:5432/salary_prediction")\
        .option("dbtable", table_name)\
        .option("user", "postgres")\
        .option("password", "postgres")\
        .save() 
    

def main(file_path: str):
    spark = (SparkSession.builder
             .appName("salary_prediction")
             .config("spark.executor.memory", "6g")
             .config("spark.driver.memory", "4g")
             .getOrCreate())
    spark.sparkContext.setLogLevel("ERROR")
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    df = filter_and_drop_rows(df)
    df = clean_data(df)
    df.write.csv("output_directory", mode="overwrite", header=True)
    to_postgres(df, "developer_survey_2024")
    spark.stop()

if __name__ == "__main__":
    main("test.csv")