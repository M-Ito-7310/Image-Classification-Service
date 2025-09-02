"""Database indexes and optimization configurations."""

from sqlalchemy import Index, text
from sqlalchemy.engine import Engine
from app.core.database import engine
import logging

logger = logging.getLogger(__name__)

# Define indexes for performance optimization
DATABASE_INDEXES = [
    # User table indexes
    Index('idx_users_email_active', 'users.email', 'users.is_active'),
    Index('idx_users_username_active', 'users.username', 'users.is_active'),
    Index('idx_users_created_at', 'users.created_at'),
    Index('idx_users_last_login', 'users.last_login'),
    
    # Classification records indexes
    Index('idx_classification_records_user_id', 'classification_records.user_id'),
    Index('idx_classification_records_created_at', 'classification_records.created_at'),
    Index('idx_classification_records_model_name', 'classification_records.model_name'),
    Index('idx_classification_records_user_created', 'classification_records.user_id', 'classification_records.created_at'),
    Index('idx_classification_records_confidence', 'classification_records.confidence_score'),
    
    # User sessions indexes
    Index('idx_user_sessions_user_id', 'user_sessions.user_id'),
    Index('idx_user_sessions_session_token', 'user_sessions.session_token'),
    Index('idx_user_sessions_refresh_token', 'user_sessions.refresh_token'),
    Index('idx_user_sessions_expires_at', 'user_sessions.expires_at'),
    Index('idx_user_sessions_active', 'user_sessions.is_active', 'user_sessions.expires_at'),
    
    # Custom models indexes
    Index('idx_custom_models_user_id', 'custom_models.user_id'),
    Index('idx_custom_models_model_id', 'custom_models.model_id'),
    Index('idx_custom_models_status', 'custom_models.status'),
    Index('idx_custom_models_user_status', 'custom_models.user_id', 'custom_models.status'),
    Index('idx_custom_models_created_at', 'custom_models.created_at'),
]

# PostgreSQL-specific optimization queries
POSTGRESQL_OPTIMIZATIONS = [
    # Enable auto-vacuum and statistics collection
    "ALTER TABLE users SET (autovacuum_enabled = true);",
    "ALTER TABLE classification_records SET (autovacuum_enabled = true);",
    "ALTER TABLE user_sessions SET (autovacuum_enabled = true);",
    "ALTER TABLE custom_models SET (autovacuum_enabled = true);",
    
    # Update statistics for better query planning
    "ANALYZE users;",
    "ANALYZE classification_records;", 
    "ANALYZE user_sessions;",
    "ANALYZE custom_models;",
    
    # Set work_mem for better sort performance
    "SET work_mem = '256MB';",
    
    # Enable parallel query execution
    "SET max_parallel_workers_per_gather = 4;",
]

def create_indexes(engine: Engine) -> bool:
    """Create database indexes for performance optimization."""
    try:
        with engine.connect() as connection:
            # Create indexes
            for index in DATABASE_INDEXES:
                try:
                    index.create(connection, checkfirst=True)
                    logger.info(f"Created index: {index.name}")
                except Exception as e:
                    logger.warning(f"Index creation failed or already exists: {index.name} - {e}")
            
            # Apply PostgreSQL-specific optimizations
            if 'postgresql' in str(engine.url):
                for query in POSTGRESQL_OPTIMIZATIONS:
                    try:
                        connection.execute(text(query))
                        logger.info(f"Applied optimization: {query[:50]}...")
                    except Exception as e:
                        logger.warning(f"Optimization failed: {query[:30]}... - {e}")
            
            connection.commit()
            logger.info("Database indexing and optimization completed successfully")
            return True
            
    except Exception as e:
        logger.error(f"Database indexing failed: {e}")
        return False

def drop_indexes(engine: Engine) -> bool:
    """Drop database indexes (for testing/migration purposes)."""
    try:
        with engine.connect() as connection:
            for index in DATABASE_INDEXES:
                try:
                    index.drop(connection, checkfirst=True)
                    logger.info(f"Dropped index: {index.name}")
                except Exception as e:
                    logger.warning(f"Index drop failed or doesn't exist: {index.name} - {e}")
            
            connection.commit()
            logger.info("Database index removal completed")
            return True
            
    except Exception as e:
        logger.error(f"Database index removal failed: {e}")
        return False

def analyze_query_performance(engine: Engine) -> dict:
    """Analyze database query performance and suggest optimizations."""
    performance_data = {}
    
    try:
        with engine.connect() as connection:
            if 'postgresql' in str(engine.url):
                # Get table sizes
                result = connection.execute(text("""
                    SELECT 
                        tablename,
                        pg_size_pretty(pg_total_relation_size(tablename::regclass)) as size,
                        pg_total_relation_size(tablename::regclass) as size_bytes
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                    ORDER BY pg_total_relation_size(tablename::regclass) DESC;
                """))
                
                performance_data['table_sizes'] = [dict(row._mapping) for row in result]
                
                # Get index usage statistics
                result = connection.execute(text("""
                    SELECT 
                        indexrelname as index_name,
                        relname as table_name,
                        idx_scan as times_used,
                        idx_tup_read as tuples_read,
                        idx_tup_fetch as tuples_fetched
                    FROM pg_stat_user_indexes 
                    ORDER BY idx_scan DESC;
                """))
                
                performance_data['index_usage'] = [dict(row._mapping) for row in result]
                
                # Get slow queries (if pg_stat_statements is enabled)
                try:
                    result = connection.execute(text("""
                        SELECT 
                            query,
                            calls,
                            total_time,
                            mean_time,
                            rows
                        FROM pg_stat_statements 
                        WHERE query NOT LIKE '%pg_stat%'
                        ORDER BY mean_time DESC 
                        LIMIT 10;
                    """))
                    performance_data['slow_queries'] = [dict(row._mapping) for row in result]
                except:
                    performance_data['slow_queries'] = "pg_stat_statements not available"
                    
        logger.info("Query performance analysis completed")
        
    except Exception as e:
        logger.error(f"Performance analysis failed: {e}")
        performance_data['error'] = str(e)
    
    return performance_data

def optimize_database() -> bool:
    """Run complete database optimization."""
    logger.info("Starting database optimization...")
    
    success = create_indexes(engine)
    if success:
        performance = analyze_query_performance(engine)
        logger.info(f"Database optimization completed. Performance data: {performance}")
    
    return success

if __name__ == "__main__":
    # Run optimization when script is executed directly
    optimize_database()