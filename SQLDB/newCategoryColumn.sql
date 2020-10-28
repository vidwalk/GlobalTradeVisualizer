ALTER TABLE [python_db].[dbo].[Product]
ADD HS2 nvarchar(2);

ALTER TABLE [python_db].[dbo].[Product]
ADD HS4 nvarchar(4);

UPDATE [python_db].[dbo].[Product]
SET HS2 = SUBSTRING(ProductID, 0, 3),HS4 = SUBSTRING(ProductID, 0, 5)
WHERE LEN(ProductID) > 2 


ALTER TABLE [python_db].[dbo].[Product]
ADD Category int;

ALTER TABLE [python_db].[dbo].[Product]
ADD CategoryText nvarchar(35);

UPDATE [python_db].[dbo].[Product]
SET Category = 1,CategoryText = 'Agriculture'
WHERE ProductId >= '01' and ProductId <= '24'

UPDATE [python_db].[dbo].[Product]
SET Category = 2,CategoryText = 'Industry'
 WHERE (ProductId >= '25' and ProductId <= '31') or (ProductID >= '35' and ProductID <='36') or (ProductID >= '38' and ProductID <='40') or (ProductID = '45') or (ProductID >= '72' and ProductID <='89') 

UPDATE [python_db].[dbo].[Product]
SET Category = 3,CategoryText = 'Commodities'
 WHERE (ProductId >= '32' and ProductId <= '34') or (ProductID = '37') or (ProductID = '49') or (ProductId >= '64' and ProductId <= '66') or (ProductId >= '90' and ProductId <= '99')  

UPDATE [python_db].[dbo].[Product]
SET Category = 4,CategoryText = 'Materials'
 WHERE (ProductId >= '41' and ProductId <= '44') or (ProductId >= '46' and ProductId <= '48') or (ProductId >= '50' and ProductId <= '63') or (ProductId >= '67' and ProductId <= '71')   