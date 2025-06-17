from typing import List, Dict, Any, Optional
from .database import DatabaseConnection
import logging
import asyncio

logger = logging.getLogger(__name__)

class GoldViews:
    """Model for gold layer views"""
    
    @staticmethod
    async def get_top_product(limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get top products from gold view"""
        try:
            async with DatabaseConnection() as db:
                query = "SELECT * FROM gold.fact_sale"
                
                if limit:
                    query += f" OFFSET 0 ROWS FETCH NEXT {limit} ROWS ONLY"
                
                data = await db.execute_query_async(query)
                
                # Process the data to get product frequencies
                productFreq = {}
                for row in data:
                    product_id = row.get('product_id')
                    if product_id is not None:
                        productFreq[product_id] = productFreq.get(product_id, 0) + 1
                
                # Sort by frequency (descending)
                productFreq = sorted(productFreq.items(), key=lambda x: x[1], reverse=True)
                
                # Get product names and create result
                result = []
                for product_id, frequency in productFreq:
                    if product_id is None:
                        continue
                    
                    # Get product name
                    name_query = f"SELECT product_name, brand_name, price FROM gold.dim_product WHERE product_id = {product_id}"
                    name_data = await db.execute_query_async(name_query)
                    
                    if name_data:
                        result.append({
                            "product_id": product_id,
                            "product_name": name_data[0]['product_name'],
                            "brand_name": name_data[0]['brand_name'],
                            "price": name_data[0]['price'],
                            "frequency": frequency
                        })
                
                return result
                
        except Exception as e:
            logger.error(f"Error fetching data from gold.top_product view: {str(e)}")
            raise
    
    @staticmethod
    async def get_top_provider(limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get top providers from gold view"""
        try:
            async with DatabaseConnection() as db:
                query = "SELECT * FROM gold.top_provider"
                
                if limit:
                    query += f" OFFSET 0 ROWS FETCH NEXT {limit} ROWS ONLY"
                
                return await db.execute_query_async(query)
        except Exception as e:
            logger.error(f"Error fetching data from gold.top_provider view: {str(e)}")
            raise
    
    @staticmethod
    async def get_top_new_user_province(limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get top new user province from gold view"""
        try:
            async with DatabaseConnection() as db:
                query = "SELECT * FROM gold.dim_user"
                
                if limit:
                    query += f" OFFSET 0 ROWS FETCH NEXT {limit} ROWS ONLY"
                data = await db.execute_query_async(query)
                list_province = {}
                for row in data:
                    province = row['city'] + "," + row['district']
                    if province is not None:
                        list_province[province] = list_province.get(province, 0) + 1
                list_province = sorted(list_province.items(), key=lambda x: x[1], reverse=True)
                result = []
                for province, count in list_province:
                    result.append({
                        "province": province,
                        "count": count
                    })
                return result
        except Exception as e:
            logger.error(f"Error fetching data from gold.top_new_user_province view: {str(e)}")
            raise
    
    @staticmethod
    async def get_available_views() -> List[str]:
        """Get list of available gold views"""
        try:
            async with DatabaseConnection() as db:
                query = """
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.VIEWS 
                WHERE TABLE_SCHEMA = 'gold'
                ORDER BY TABLE_NAME
                """
                results = await db.execute_query_async(query)
                return [row['TABLE_NAME'] for row in results]
        except Exception as e:
            logger.error(f"Error getting available gold views: {str(e)}")
            raise
    
    @staticmethod
    async def get_view_schema(view_name: str) -> List[Dict[str, Any]]:
        """Get schema information for a specific gold view"""
        try:
            async with DatabaseConnection() as db:
                query = """
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = 'gold' 
                AND TABLE_NAME = ?
                ORDER BY ORDINAL_POSITION
                """
                return await db.execute_query_async(query, (view_name,))
        except Exception as e:
            logger.error(f"Error getting schema for gold view {view_name}: {str(e)}")
            raise
    
    @staticmethod
    async def get_view_data(view_name: str, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get data from any gold view by name"""
        try:
            async with DatabaseConnection() as db:
                query = f"SELECT * FROM gold.{view_name}"
                
                if limit:
                    query += f" OFFSET {offset or 0} ROWS FETCH NEXT {limit} ROWS ONLY"
                
                return await db.execute_query_async(query)
        except Exception as e:
            logger.error(f"Error fetching data from gold view {view_name}: {str(e)}")
            raise
    
    @staticmethod
    async def get_view_count(view_name: str) -> int:
        """Get total count of records in a gold view"""
        try:
            async with DatabaseConnection() as db:
                query = f"SELECT COUNT(*) as count FROM gold.{view_name}"
                results = await db.execute_query_async(query)
                return results[0]['count'] if results else 0
        except Exception as e:
            logger.error(f"Error getting count from gold view {view_name}: {str(e)}")
            raise 