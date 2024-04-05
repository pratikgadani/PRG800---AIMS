USE [Temp_Project]
GO

/****** Object:  Table [dbo].[User_data]    Script Date: 2024-04-05 5:44:37 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[User_data](
	[id] [nvarchar](50) NOT NULL,
	[password] [nvarchar](50) NOT NULL,
	[access_level] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_User_data] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

