from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import FloatType, IntegerType
import requests
import os

JDBC_URL  = "jdbc:postgresql://postgres:5432/stack-overflow-survey"
JDBC_OPTS = {"user": "postgres", "password": "postgres", "driver": "org.postgresql.Driver"}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JDBC_JAR_PATH = os.path.join(BASE_DIR, "postgresql-42.7.6.jar")

spark = (SparkSession.builder
        .appName("salary_prediction")
        .config("spark.executor.memory", "6g")
        .config("spark.driver.memory", "4g")
        .config("spark.jars", JDBC_JAR_PATH)
        .getOrCreate())
spark.sparkContext.setLogLevel("ERROR")

def read_table(table_name: str):
    return (spark.read
            .format("jdbc")
            .options(**JDBC_OPTS, url=JDBC_URL, dbtable=table_name)
            .load())

def write_table(df, table_name: str, mode="append"):
    (df.write
       .format("jdbc")
       .options(**JDBC_OPTS, url=JDBC_URL, dbtable=table_name)
       .mode(mode)
       .save())

def filter_and_drop_rows(df):
    # remove invalid respondents and check compensation is not NA
    filtered_df = df.filter(
        (df.Check == "Apples")&
        (df.MainBranch == "I am a developer by profession")&
        ((df.Employment == "Employed, full-time") | 
         (df.Employment == "Employed, part-time") |
         (df.Employment == "Independent contractor, freelancer, or self-employed"))&
        (df.CompTotal != "NA"))

    columns_to_drop = [
        "MainBranch","Check","CodingActivities","LearnCodeOnline","TechDoc","PurchaseInfluence","BuyNewTool","BuildvsBuy","TechEndorse",
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
    ]
    columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    dropped_df = filtered_df.drop(*columns_to_drop)
    return dropped_df

def clean_data(df):
    URL = "https://openexchangerates.org/api/latest.json"
    params = {"app_id": "a82429fa6fdb42f8855e6efc1d92e60c"}
    conversion_rates = requests.get(URL, params=params).json()["rates"]

    def convert_to_USD(currency, amount):
        try: 
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
        except (ValueError, TypeError):
            return None
        
    convert_to_usd_udf = F.udf(convert_to_USD, FloatType())

    cleaned_df = (
        df
        .withColumn("CompTotal(USD)", 
                    F.when( ((F.col("Currency").isNull()) | 
                            (F.col("Currency") == "NA") |
                            (F.col("CompTotal") == "None") |
                           (F.col("CompTotal").isNull())), F.lit(None))
                    .otherwise(convert_to_usd_udf(F.col("Currency"), F.col("CompTotal"))))
        .withColumn("YearsCode", 
                    F.when( ((F.col("YearsCode")=="NA") | (F.col("YearsCode").isNull())), F.lit(None))
                    .otherwise(F.col("YearsCode").cast(IntegerType())))
        .withColumn("WorkExp",
                    F.when( ((F.col("WorkExp")=="NA") | (F.col("WorkExp").isNull())), F.lit(None))
                    .otherwise(F.col("WorkExp").cast(IntegerType())))
        .withColumn("LanguageCount",
                    F.size(F.array_remove(F.split(F.col("LanguageHaveWorkedWith"), ";"))))
        .withColumn("DatabaseCount",
                    F.size(F.array_remove(F.split(F.col("DatabaseHaveWorkedWith"), ";"))))
        .withColumn("CloudCount",
                    F.size(F.array_remove(F.split(F.col("PlatformHaveWorkedWith"), ";"))))
        .withColumn("WebframeCount",
                    F.size(F.array_remove(F.split(F.col("WebframeHaveWorkedWith"), ";"))))
        .withColumn("EmbeddedCount",
                    F.size(F.array_remove(F.split(F.col("EmbeddedHaveWorkedWith"), ";"))))
        .withColumn("MiscTechCount",
                    F.size(F.array_remove(F.split(F.col("MiscTechHaveWorkedWith"), ";"))))
        .withColumn("DevToolCount",
                    F.size(F.array_remove(F.split(F.col("ToolsTechHaveWorkedWith"), ";"))))
        .withColumn("CollabToolsCount",
                    F.size(F.array_remove(F.split(F.col("NEWCollabToolsHaveWorkedWith"), ";"))))
        .withColumn("OpSysCount",
                    F.size(F.array_remove(F.split(F.col("OpSysProfessional use"), ";"))))
        .withColumn("AISearchDevCount",
                    F.size(F.array_remove(F.split(F.col("AISearchDevHaveWorkedWith"), ";"))))
    )
    # filtering after transformation
    cleaned_df = cleaned_df.filter(
        ~((F.col("CompTotal(USD)").isNull())|(F.col("CompTotal(USD)") == float("inf"))|(F.col("CompTotal(USD)") > float("1E6")))
    )
    return cleaned_df

def write_fact_table(df):
    fact_attr = [
        "ResponseId","Age","Employment","RemoteWork","EdLevel","YearsCode","YearsCodePro","DevType","OrgSize","Country","Currency","CompTotal",
        "LanguageCount","DatabaseCount","CloudCount","WebframeCount","EmbeddedCount","MiscTechCount","DevToolCount","CollabToolsCount",
        "OpSysCount","AISearchDevCount","AISelect","AISent","AIAcc","AIComplex","AIThreat","ICorPM","WorkExp","Industry","CompTotal(USD)"
    ]
    fact_df = df.select(*fact_attr)
    write_table(fact_df, "Respondent")
    fact_attr.remove("ResponseId")
    dim_df = df.drop(*fact_attr)
    return dim_df

def split_and_write_dim_table(
        source_df,               
        column_name,             # e.g. "LanguageHaveWorkedWith"
        dim_table,               # e.g. "language"
        bridge_table             # "respondent_language"
):
    dim_df = read_table(dim_table).select(
                 F.col("name").alias("dim_name"), F.col("id"))
    # explode the multiselect list to rows
    exploded = (source_df
        .select("ResponseId",
                F.explode(F.split(F.col(column_name), ";")).alias("item"))
        .withColumn("item", F.trim("item"))
        .filter("item <> ''"))
    # join dimension table to exploded items
    # dim_name | id | item | ResponseId
    bridged = (exploded
               .join(F.broadcast(dim_df), exploded.item == dim_df.dim_name, "left"))
    
    bridged = bridged.filter(F.col("id").isNotNull()).select("ResponseId", "id").distinct()
    write_table(bridged, bridge_table)

def main(file_path: str):
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    df = filter_and_drop_rows(df)
    df = clean_data(df)

    dim_df = write_fact_table(df)
    split_and_write_dim_table(dim_df, "LearnCode", "LearnCode", "RespondentLearnCode")
    split_and_write_dim_table(dim_df, "LanguageHaveWorkedWith", "ProgrammingLanguage", "RespondentLanguage")
    split_and_write_dim_table(dim_df, "DatabaseHaveWorkedWith", "Database", "RespondentDatabase")
    split_and_write_dim_table(dim_df, "PlatformHaveWorkedWith", "Cloud", "RespondentCloud")
    split_and_write_dim_table(dim_df, "WebframeHaveWorkedWith", "WebFramework", "RespondentWebFramework")
    split_and_write_dim_table(dim_df, "EmbeddedHaveWorkedWith", "EmbeddedSystem", "RespondentEmbeddedSystem")
    split_and_write_dim_table(dim_df, "MiscTechHaveWorkedWith", "MiscTech", "RespondentMiscTech")
    split_and_write_dim_table(dim_df, "ToolsTechHaveWorkedWith", "DevTool", "RespondentDevTool")
    split_and_write_dim_table(dim_df, "NEWCollabToolsHaveWorkedWith", "IDE", "RespondentIDE")
    split_and_write_dim_table(dim_df, "OpSysProfessional use", "OS", "RespondentOS")
    split_and_write_dim_table(dim_df, "AISearchDevHaveWorkedWith", "AITool", "RespondentAITool")
    split_and_write_dim_table(dim_df, "AIToolCurrently Using", "DevWorkflow", "RespondentAIDevWorkflowUsing")
    split_and_write_dim_table(dim_df, "AIToolInterested in Using", "DevWorkflow", "RespondentAIDevWorkflowInterested") 
    split_and_write_dim_table(dim_df, "AIToolNot interested in Using", "DevWorkflow", "RespondentAIDevWorkflowNotInterested") 

    spark.stop()

if __name__ == "__main__":
    import sys
    file_path = sys.argv[1] 
    main(file_path)