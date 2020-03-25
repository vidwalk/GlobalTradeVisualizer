USE python_db
BEGIN TRANSACTION [Tran1]

	BEGIN TRY

        CREATE TABLE Country(
        "CountryID" int IDENTITY(1,1) PRIMARY KEY,
        "Name" nvarchar(30))
        CREATE TABLE Date(
        "DateID" int IDENTITY(1,1) PRIMARY KEY,
        "Date" date)
        CREATE TABLE Product(
        "ProductID" int IDENTITY(1,1) PRIMARY KEY,
        "Name" nvarchar(30))
        CREATE TABLE TradeLine(
        "ID" int identity(1,1) PRIMARY KEY,
        "ProductID" int,
        "DateID" int,
        "ReporterID" int,
        "PartnerID" int,
        "QTY" DECIMAL(10,2),
        "Amount" DECIMAL(10,2),
        FOREIGN KEY ("ProductID") REFERENCES Product("ProductID"),
        FOREIGN KEY ("DateID") REFERENCES Date("DateID"),
        FOREIGN KEY ("ReporterID") REFERENCES Country("CountryID"),
        FOREIGN KEY ("PartnerID") REFERENCES Country("CountryID"))
	    COMMIT TRANSACTION [Tran1]
    END TRY

    BEGIN CATCH

      ROLLBACK TRANSACTION [Tran1]

    END CATCH  
GO
BEGIN TRANSACTION [Tran2]

	BEGIN TRY
        INSERT INTO "Country" VALUES('USA');
        INSERT INTO "Country" VALUES('China');
        INSERT INTO "Product" VALUES('hair and bristles');
        INSERT INTO "Date" VALUES('2018-12-31');
        INSERT INTO "TradeLine" VALUES(3,1,1,2,1644640,24496.81);
        COMMIT TRANSACTION [Tran2]
    END TRY

    BEGIN CATCH

      ROLLBACK TRANSACTION [Tran2]

    END CATCH 
GO

SELECT r.Name as Reporter,p.Name as Partner,Product.Name as Product,"Date".Date, QTY as Quantity,Amount 
FROM TradeLine
JOIN Country as p ON TradeLine.PartnerID = p.CountryID
JOIN Country as r ON TradeLine.ReporterID = r.CountryID
JOIN Product  ON TradeLine.ProductID = Product.ProductID
JOIN "Date" on TradeLine.DateID = "Date".DateID