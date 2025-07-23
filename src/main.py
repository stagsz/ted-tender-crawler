#!/usr/bin/env python3
"""
TED.EU Tender Search Actor
Generic actor for searching European public procurement tenders with
customizable filtering
"""

import asyncio
import logging
from datetime import datetime
from apify import Actor
from ted_search_engine import TEDSearchEngine, IndustryTemplates

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    async with Actor:
        # Get actor input
        actor_input = await Actor.get_input() or {}
        
        Actor.log.info("=== TED.EU Tender Search Actor Started ===")
        Actor.log.info(f"Input received: {len(str(actor_input))} characters")
        
        # Apply industry template if specified
        if actor_input.get('industryTemplate', 'custom') != 'custom':
            template = actor_input['industryTemplate']
            Actor.log.info(f"Applying industry template: {template}")
            
            template_keywords = IndustryTemplates.get_keywords(template)
            template_cpv = IndustryTemplates.get_cpv_codes(template)
            
            if template_keywords:
                actor_input['searchKeywords'] = template_keywords
            if template_cpv:
                actor_input['cpvCodes'] = template_cpv
        
        # Validate and set defaults
        search_keywords = actor_input.get('searchKeywords', ['consulting', 'services'])
        cpv_codes = actor_input.get('cpvCodes', [])
        countries = actor_input.get('countries', ['DE', 'FR', 'IT'])
        year_from = actor_input.get('yearFrom', 2024)
        year_to = actor_input.get('yearTo', 2024)
        active_only = actor_input.get('activeOnly', False)
        min_value = actor_input.get('minValue', 0)
        max_results = actor_input.get('maxResults', 100)
        output_format = actor_input.get('outputFormat', 'json')
        include_documents = actor_input.get('includeDocuments', True)
        scoring_criteria = actor_input.get('scoringCriteria', {
            'keywordMatch': 40,
            'cpvMatch': 30, 
            'countryMatch': 20,
            'valueMatch': 10
        })
        
        # Log search parameters
        Actor.log.info(f"Search Keywords: {search_keywords}")
        Actor.log.info(f"CPV Codes: {cpv_codes}")
        Actor.log.info(f"Countries: {countries}")
        Actor.log.info(f"Date Range: {year_from}-{year_to}")
        Actor.log.info(f"Active Only: {active_only}")
        Actor.log.info(f"Max Results: {max_results}")
        
        # Initialize search engine
        search_engine = TEDSearchEngine()
        search_engine.set_scoring_criteria(scoring_criteria)
        
        try:
            # Execute search
            Actor.log.info("Starting TED.EU search...")
            results = await search_engine.search_tenders(
                keywords=search_keywords,
                cpv_codes=cpv_codes,
                countries=countries,
                year_from=year_from,
                year_to=year_to,
                active_only=active_only,
                min_value=min_value,
                max_results=max_results,
                include_documents=include_documents
            )
            
            Actor.log.info(f"Found {len(results)} tenders")
            
            # Process and push results
            processed_count = 0
            for result in results:
                await Actor.push_data(result)
                processed_count += 1
                
                # Log progress every 10 items
                if processed_count % 10 == 0:
                    Actor.log.info(f"Processed {processed_count}/{len(results)} tenders")
            
            # Summary statistics
            if results:
                avg_score = sum(r['relevance_score'] for r in results) / len(results)
                high_relevance = len([r for r in results if r['relevance_score'] > 70])
                active_tenders = len([r for r in results if r['status'] == 'active'])
                
                Actor.log.info(f"=== SEARCH SUMMARY ===")
                Actor.log.info(f"Total tenders found: {len(results)}")
                Actor.log.info(f"Average relevance score: {avg_score:.1f}")
                Actor.log.info(f"High relevance tenders (>70): {high_relevance}")
                Actor.log.info(f"Active tenders: {active_tenders}")
                
                # Push summary data
                await Actor.push_data({
                    '_summary': True,
                    'total_found': len(results),
                    'average_score': round(avg_score, 1),
                    'high_relevance_count': high_relevance,
                    'active_count': active_tenders,
                    'search_timestamp': datetime.now().isoformat(),
                    'search_parameters': {
                        'keywords': search_keywords,
                        'countries': countries,
                        'date_range': f"{year_from}-{year_to}",
                        'active_only': active_only
                    }
                })
            else:
                Actor.log.info("No tenders found matching criteria")
                
        except Exception as e:
            Actor.log.error(f"Error during search: {e}")
            await Actor.fail(f"TED search failed: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())