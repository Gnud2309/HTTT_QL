# Use the official Microsoft SQL Server 2022 image as base
FROM mcr.microsoft.com/mssql/server:2022-latest

# Set environment variables
ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=ShopApp@DW2025

# Expose SQL Server port
EXPOSE 1433

# Default command to run SQL Server
CMD ["/opt/mssql/bin/sqlservr"]
