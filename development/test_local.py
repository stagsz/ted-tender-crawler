#!/usr/bin/env python3
"""
Local test script for TED.EU Actor
Test the actor functionality without Apify platform
"""

import asyncio
import json
import logging
from datetime import datetime
from ted_search_engine import TEDSearchEngine, IndustryTemplates

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_basic_search():
    """Test basic search functionality"""
    print("=== Testing Basic Search ===")
    
    # Test configuration
    test_input = {
        "searchKeywords": ["IT services", "software development"],
        "countries": ["DE", "FR"],
        "yearFrom": 2024,
        "yearTo": 2024,
        "activeOnly": False,
        "maxResults": 10
    }
    
    print(f"Test input: {json.dumps(test_input, indent=2)}")
    
    # Initialize search engine
    search_engine = TEDSearchEngine()
    
    try:
        results = await search_engine.search_tenders(
            keywords=test_input["searchKeywords"],
            cpv_codes=[],
            countries=test_input["countries"], 
            year_from=test_input["yearFrom"],
            year_to=test_input["yearTo"],
            active_only=test_input["activeOnly"],
            min_value=0,
            max_results=test_input["maxResults"],
            include_documents=True
        )
        
        print(f"\n✅ Search completed: {len(results)} results")
        
        if results:
            print("\n📋 Sample Results:")
            for i, result in enumerate(results[:3], 1):
                print(f"\n{i}. {result['title'][:80]}...")
                print(f"   Buyer: {result['buyer_name'][:50]}")
                print(f"   Country: {result['country']}")
                print(f"   Score: {result['relevance_score']}")
                print(f"   Status: {result['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def test_industry_template():
    """Test industry template functionality"""
    print("\n=== Testing Industry Templates ===")
    
    # Test IT template
    template = "it-software"
    keywords = IndustryTemplates.get_keywords(template)
    cpv_codes = IndustryTemplates.get_cpv_codes(template)
    
    print(f"Template: {template}")
    print(f"Keywords: {keywords[:5]}...")  # Show first 5
    print(f"CPV Codes: {cpv_codes[:3]}...")  # Show first 3
    
    search_engine = TEDSearchEngine()
    
    try:
        results = await search_engine.search_tenders(
            keywords=keywords[:3],  # Use first 3 keywords for faster test
            cpv_codes=cpv_codes[:2],  # Use first 2 CPV codes
            countries=["DE"],
            year_from=2024,
            year_to=2024,
            active_only=True,
            min_value=0,
            max_results=5,
            include_documents=False
        )
        
        print(f"✅ Template search completed: {len(results)} results")
        return True
        
    except Exception as e:
        print(f"❌ Template test failed: {e}")
        return False

async def test_custom_scoring():
    """Test custom scoring criteria"""
    print("\n=== Testing Custom Scoring ===")
    
    search_engine = TEDSearchEngine()
    
    # Set custom scoring criteria
    custom_criteria = {
        'keywordMatch': 50,
        'cpvMatch': 20,
        'countryMatch': 20,
        'valueMatch': 10
    }
    search_engine.set_scoring_criteria(custom_criteria)
    
    try:
        results = await search_engine.search_tenders(
            keywords=["consulting"],
            cpv_codes=["79400000"],
            countries=["DE", "FR"],
            year_from=2024,
            year_to=2024,
            active_only=False,
            min_value=10000,
            max_results=5,
            include_documents=True
        )
        
        print(f"✅ Custom scoring test completed: {len(results)} results")
        
        if results:
            avg_score = sum(r['relevance_score'] for r in results) / len(results)
            print(f"Average relevance score: {avg_score:.1f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Custom scoring test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 TED.EU Actor Local Testing")
    print("=" * 50)
    
    tests = [
        test_basic_search,
        test_industry_template,
        test_custom_scoring
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All tests passed! Actor is ready for deployment.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())