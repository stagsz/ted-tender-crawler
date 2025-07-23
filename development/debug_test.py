#!/usr/bin/env python3
"""
Debug test script to understand why results are being filtered out
"""

import asyncio
import json
import logging
from datetime import datetime
from ted_search_engine import TEDSearchEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def debug_filtering():
    """Debug the filtering logic"""
    print("🔍 TED.EU Debug Test")
    print("====================")
    
    # Initialize search engine
    search_engine = TEDSearchEngine()
    
    try:
        # Test with activeOnly=False to see if that's the issue
        results = await search_engine.search_tenders(
            keywords=["consulting"],
            cpv_codes=[],
            countries=["DE"],
            year_from=2024,
            year_to=2024,
            active_only=False,  # Disable active filter
            min_value=0,       # No minimum value
            max_results=5,
            include_documents=True
        )
        
        print(f"\n📊 Results with activeOnly=False: {len(results)}")
        
        if results:
            # Show sample result
            sample = results[0]
            print(f"\n📋 Sample result:")
            print(f"  Title: {sample.get('title', 'N/A')}")
            print(f"  Buyer: {sample.get('buyer_name', 'N/A')}")
            print(f"  Country: {sample.get('country', 'N/A')}")
            print(f"  Status: {sample.get('status', 'N/A')}")
            print(f"  Deadline: {sample.get('deadline_date', 'N/A')}")
            print(f"  Value: {sample.get('estimated_value_eur', 'N/A')}")
            print(f"  Score: {sample.get('relevance_score', 'N/A')}")
        else:
            print("\n⚠️ Still no results - let's check raw processing...")
            
            # Let's inspect what happens during processing
            await debug_raw_processing(search_engine)
            
    except Exception as e:
        logger.error(f"Debug test failed: {e}")
        import traceback
        traceback.print_exc()

async def debug_raw_processing(search_engine):
    """Debug the raw processing step"""
    print("\n🔍 Debugging raw processing...")
    
    # Build a simple query
    search_queries = search_engine._build_search_queries(
        keywords=["consulting"],
        cpv_codes=[],
        countries=["DE"],
        year_from=2024,
        year_to=2024,
        min_value=0
    )
    
    # Get raw results from first query
    if search_queries:
        raw_results = await search_engine._execute_search(search_queries[0])
        print(f"📊 Raw results from API: {len(raw_results)}")
        
        if raw_results:
            # Show first raw result structure
            first_raw = raw_results[0]
            print(f"\n📋 First raw result fields:")
            for key, value in first_raw.items():
                if key.startswith('_'):
                    continue  # Skip metadata
                print(f"  {key}: {type(value)} = {str(value)[:100]}...")
            
            # Remove duplicates
            unique_results = search_engine._remove_duplicates(raw_results)
            print(f"\n📊 After deduplication: {len(unique_results)}")
            
            # Try processing one result manually
            if unique_results:
                print(f"\n🔧 Processing first result...")
                try:
                    result = unique_results[0]
                    
                    # Extract basic info manually
                    tender_info = {
                        'notice_id': result.get('notice-identifier', ''),
                        'title': search_engine._safe_get_text(result, 'notice-title'),
                        'buyer_name': search_engine._safe_get_text(result, 'buyer-name'),
                        'country': result.get('buyer-country', ''),
                        'publication_date': result.get('publication-date', ''),
                        'deadline_date': result.get('deadline-receipt', ''),
                        'estimated_value_eur': search_engine._extract_value(result),
                        'status': 'unknown'  # Default for now
                    }
                    
                    print(f"  ✅ Extracted tender info:")
                    for key, value in tender_info.items():
                        print(f"    {key}: {value}")
                    
                    # Check what fields are actually in the result
                    print(f"\n📋 Available fields in API response:")
                    for field in sorted(result.keys()):
                        if not field.startswith('_'):
                            print(f"    {field}")
                            
                except Exception as e:
                    print(f"  ❌ Processing failed: {e}")
                    import traceback
                    traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_filtering())