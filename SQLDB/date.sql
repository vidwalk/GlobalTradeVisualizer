DECLARE @StartDate DATE
DECLARE @EndDate DATE
SET @StartDate = '1996-01-01'
SET @EndDate = '2018-12-31'
WHILE @StartDate <= @EndDate
BEGIN
INSERT INTO [Dates]
(
DateID
,Year
,Month
)
SELECT
@StartDate
,YEAR(@StartDate)
,MONTH(@StartDate)
SET @StartDate = DATEADD(mm, 1, @StartDate)
END