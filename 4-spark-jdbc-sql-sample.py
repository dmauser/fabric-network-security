# Spark JDBC write to Azure SQL Database
# Using Managed Private Endpoint from Microsoft Fabric

jdbc_hostname = "mausermsdn.database.windows.net"
jdbc_port = 1433
jdbc_database = "mauserdb"

jdbc_url = (
    f"jdbc:sqlserver://{jdbc_hostname}:{jdbc_port};"
    f"database={jdbc_database};"
    "encrypt=true;"
    "trustServerCertificate=false;"
    "hostNameInCertificate=*.database.windows.net;"
    "loginTimeout=30;"
)

target_table = "dbo.SalesFacts"

# Sample DataFrame
df = spark.createDataFrame(
    [(1, "Order-001", 120.50), (2, "Order-002", 89.30)],
    ["id", "order_id", "amount"]
)

(
    df.write
      .format("jdbc")
      .option("url", jdbc_url)
      .option("dbtable", target_table)
      .option("user", "<sql-username>")
      .option("password", "<sql-password>")  # store in secret in real workloads
      .mode("append")
      .save()
)

print("Write to Azure SQL Database completed successfully.")