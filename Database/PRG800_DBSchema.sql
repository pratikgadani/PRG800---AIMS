USE [Temp_Project]
GO

/****** Object:  Table [dbo].[Table_data]    Script Date: 2024-03-21 1:03:14 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Table_data](
	[Sr_No] [int] NULL,
	[Barcode_Number] [nvarchar](50) NULL,
	[Product_Name] [nchar](10) NULL,
	[Total_Quantity] [numeric](18, 0) NULL,
	[Remaining_Quantity] [numeric](18, 0) NULL
) ON [PRIMARY]
GO

