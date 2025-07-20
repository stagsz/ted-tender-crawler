#!/usr/bin/env python3
"""
Generic TED.EU Search Engine
Adapted from specialized version to be configurable for any industry/keywords
"""

import requests
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
import json
import re

logger = logging.getLogger(__name__)

class IndustryTemplates:
    """Pre-defined keyword and CPV code templates for common industries"""
    
    TEMPLATES = {
        'it-software': {
            'keywords': [
                'software development', 'IT services', 'system integration', 
                'cloud services', 'database', 'web development', 'mobile app',
                'cybersecurity', 'data analytics', 'artificial intelligence',
                'machine learning', 'digital transformation', 'ERP system'
            ],
            'cpv_codes': [
                '72000000',  # IT services
                '72100000',  # Hardware consultancy services  
                '72200000',  # Software programming services
                '72300000',  # Data services
                '72400000',  # Internet services
                '72500000',  # Computer-related services
                '72600000'   # Computer support services
            ]
        },
        'construction': {
            'keywords': [
                'construction', 'building', 'renovation', 'infrastructure',
                'road construction', 'bridge', 'civil engineering', 'architecture',
                'project management', 'facility management', 'maintenance',
                'electrical installation', 'plumbing', 'HVAC installation'
            ],
            'cpv_codes': [
                '45000000',  # Construction work
                '45100000',  # Site preparation
                '45200000',  # Building construction work
                '45300000',  # Building installation work
                '45400000',  # Building completion work
                '45500000'   # Hiring of construction equipment
            ]
        },
        'healthcare': {
            'keywords': [
                'medical equipment', 'healthcare services', 'hospital', 'medical supplies',
                'pharmaceutical', 'medical devices', 'laboratory equipment',
                'diagnostic equipment', 'patient care', 'medical software',
                'telemedicine', 'health information system'
            ],
            'cpv_codes': [
                '33000000',  # Medical equipment and pharmaceuticals
                '33100000',  # Medical equipment
                '33600000',  # Pharmaceutical products
                '85100000',  # Health services
                '85110000',  # Hospital services
                '85200000'   # Veterinary services
            ]
        },
        'consulting': {
            'keywords': [
                'consulting services', 'management consulting', 'business consulting',
                'strategic planning', 'process improvement', 'organizational development',
                'change management', 'project management', 'advisory services',
                'feasibility study', 'market research', 'business analysis'
            ],
            'cpv_codes': [
                '73000000',  # Research and development services
                '73100000',  # Research and experimental development services
                '73200000',  # Research services
                '79000000',  # Business services
                '79400000',  # Business and management consultancy services
                '79500000'   # Office-support services
            ]
        },
        'engineering': {
            'keywords': [
                'engineering services', 'technical consulting', 'design services',
                'mechanical engineering', 'electrical engineering', 'civil engineering',
                'environmental engineering', 'project engineering', 'system design',
                'technical documentation', 'feasibility study', 'technical support'
            ],
            'cpv_codes': [
                '71000000',  # Architectural, construction, engineering services
                '71200000',  # Architectural and related services
                '71300000',  # Engineering services
                '71400000',  # Urban planning and landscape services
                '71500000',  # Construction-related services
                '71600000'   # Technical testing and analysis services
            ]
        },
        'environmental': {
            'keywords': [
                'environmental services', 'waste management', 'water treatment',
                'environmental consulting', 'pollution control', 'renewable energy',
                'sustainability', 'environmental monitoring', 'remediation',
                'recycling', 'air quality', 'environmental impact assessment'
            ],
            'cpv_codes': [
                '90000000',  # Sewage, refuse, cleaning services
                '90100000',  # Sewerage services
                '90200000',  # Refuse collection services
                '90300000',  # Cleaning services
                '90700000',  # Environmental services
                '90900000'   # Cleaning and environmental services
            ]
        },
        'education': {
            'keywords': [
                'educational services', 'training', 'e-learning', 'curriculum development',
                'educational technology', 'learning management system', 'assessment',
                'educational consulting', 'teacher training', 'educational materials',
                'distance learning', 'educational software'
            ],
            'cpv_codes': [
                '80000000',  # Education and training services
                '80100000',  # Primary education services
                '80200000',  # Secondary education services
                '80300000',  # Higher education services
                '80400000',  # Adult and other education services
                '80500000'   # Training services
            ]
        },
        'transportation': {
            'keywords': [
                'transportation services', 'logistics', 'fleet management',
                'public transport', 'vehicle maintenance', 'traffic management',
                'transport planning', 'mobility services', 'freight transport',
                'passenger transport', 'transport infrastructure'
            ],
            'cpv_codes': [
                '60000000',  # Transport services
                '60100000',  # Road transport services
                '60200000',  # Public road transport services
                '60400000',  # Postal and courier services
                '60500000',  # Transport supporting services
                '34000000'   # Transport equipment
            ]
        },
        'energy': {
            'keywords': [
                'energy services', 'renewable energy', 'solar power', 'wind energy',
                'energy efficiency', 'power generation', 'electricity', 'gas supply',
                'energy management', 'smart grid', 'battery systems', 'energy storage'
            ],
            'cpv_codes': [
                '09000000',  # Petroleum products, nuclear fuel
                '65000000',  # Utilities
                '65100000',  # Water distribution services
                '65200000',  # Gas distribution services  
                '65300000',  # Electricity distribution services
                '71310000'   # Energy-efficiency services
            ]
        }
    }
    
    @classmethod
    def get_keywords(cls, template_name: str) -> List[str]:
        """Get keywords for a template"""
        return cls.TEMPLATES.get(template_name, {}).get('keywords', [])
    
    @classmethod
    def get_cpv_codes(cls, template_name: str) -> List[str]:
        """Get CPV codes for a template"""
        return cls.TEMPLATES.get(template_name, {}).get('cpv_codes', [])
    
    @classmethod
    def list_templates(cls) -> List[str]:
        """List available templates"""
        return list(cls.TEMPLATES.keys())

class TEDSearchEngine:
    """Generic TED.EU search engine with configurable filtering"""
    
    def __init__(self):
        self.api_url = "https://api.ted.europa.eu/v3/notices/search"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "TED-Apify-Actor/1.0"
        }
        
        # Default scoring criteria
        self.scoring_criteria = {
            'keywordMatch': 40,
            'cpvMatch': 30,
            'countryMatch': 20,
            'valueMatch': 10
        }
        
        # Rate limiting
        self.request_delay = 1.0  # seconds between requests
    
    def set_scoring_criteria(self, criteria: Dict[str, int]):
        """Set custom scoring criteria weights"""
        self.scoring_criteria.update(criteria)
        logger.info(f"Updated scoring criteria: {self.scoring_criteria}")
    
    async def search_tenders(self, keywords: List[str], cpv_codes: List[str],
                           countries: List[str], year_from: int, year_to: int,
                           active_only: bool = True, min_value: int = 0,
                           max_results: int = 100, include_documents: bool = True) -> List[Dict]:
        """Main search orchestration method"""
        
        logger.info(f"Starting search with {len(keywords)} keywords, {len(cpv_codes)} CPV codes")
        
        all_results = []
        
        # Build search queries
        search_queries = self._build_search_queries(
            keywords, cpv_codes, countries, year_from, year_to, min_value
        )
        
        logger.info(f"Generated {len(search_queries)} search queries")
        
        # Execute searches with rate limiting
        for i, query in enumerate(search_queries):
            logger.info(f"Executing query {i+1}/{len(search_queries)}")
            
            try:
                results = await self._execute_search(query)
                all_results.extend(results)
                
                # Rate limiting
                if i < len(search_queries) - 1:
                    await asyncio.sleep(self.request_delay)
                    
            except Exception as e:
                logger.error(f"Query {i+1} failed: {e}")
                continue
        
        logger.info(f"Raw results collected: {len(all_results)}")
        
        # Remove duplicates
        unique_results = self._remove_duplicates(all_results)
        logger.info(f"After deduplication: {len(unique_results)}")
        
        # Process and score results
        processed_results = await self._process_and_score_results(
            unique_results, keywords, cpv_codes, countries, 
            active_only, min_value, include_documents
        )
        
        # Sort by relevance score and limit results
        processed_results.sort(key=lambda x: x['relevance_score'], reverse=True)
        final_results = processed_results[:max_results]
        
        logger.info(f"Final results: {len(final_results)}")
        return final_results
    
    def _build_search_queries(self, keywords: List[str], cpv_codes: List[str],
                            countries: List[str], year_from: int, year_to: int,
                            min_value: int) -> List[Dict]:
        """Build optimized search queries"""
        queries = []
        
        # Date range filter
        start_date = f"{year_from}-01-01"
        end_date = f"{year_to}-12-31"
        
        # Strategy 1: Keyword-based searches
        if keywords:
            # Group keywords to avoid overly complex queries
            keyword_groups = [keywords[i:i+3] for i in range(0, len(keywords), 3)]
            
            for keyword_group in keyword_groups:
                query_parts = []
                
                # Keywords in title
                keyword_queries = [f'notice-title="{kw}"' for kw in keyword_group]
                if keyword_queries:
                    query_parts.append(f"({' OR '.join(keyword_queries)})")
                
                # Country filter
                if countries:
                    country_query = ' OR '.join([f'buyer-country="{country}"' for country in countries])
                    query_parts.append(f"({country_query})")
                
                # Date range
                query_parts.append(f'publication-date>={start_date}')
                query_parts.append(f'publication-date<={end_date}')
                
                # Contract value filter
                if min_value > 0:
                    query_parts.append(f'value-eur>={min_value}')
                
                final_query = ' AND '.join(query_parts)
                queries.append({'query': final_query, 'type': 'keyword', 'group': keyword_group})
        
        # Strategy 2: CPV code-based searches
        if cpv_codes:
            cpv_groups = [cpv_codes[i:i+5] for i in range(0, len(cpv_codes), 5)]
            
            for cpv_group in cpv_groups:
                query_parts = []
                
                # CPV codes
                cpv_query = ' OR '.join([f'classification-cpv="{cpv}"' for cpv in cpv_group])
                query_parts.append(f"({cpv_query})")
                
                # Country filter
                if countries:
                    country_query = ' OR '.join([f'buyer-country="{country}"' for country in countries])
                    query_parts.append(f"({country_query})")
                
                # Date range
                query_parts.append(f'publication-date>={start_date}')
                query_parts.append(f'publication-date<={end_date}')
                
                # Contract value filter
                if min_value > 0:
                    query_parts.append(f'value-eur>={min_value}')
                
                final_query = ' AND '.join(query_parts)
                queries.append({'query': final_query, 'type': 'cpv', 'group': cpv_group})
        
        # Strategy 3: Country-focused search if no specific criteria
        if not keywords and not cpv_codes:
            for country in countries:
                query_parts = []
                query_parts.append(f'buyer-country="{country}"')
                query_parts.append(f'publication-date>={start_date}')
                query_parts.append(f'publication-date<={end_date}')
                
                if min_value > 0:
                    query_parts.append(f'value-eur>={min_value}')
                
                final_query = ' AND '.join(query_parts)
                queries.append({'query': final_query, 'type': 'country', 'group': [country]})
        
        return queries
    
    async def _execute_search(self, search_config: Dict) -> List[Dict]:
        """Execute a single search query"""
        search_params = {
            "query": search_config['query'],
            "limit": 100,
            "fields": [
                "notice-identifier", "notice-title", "buyer-name", "buyer-country",
                "publication-date", "publication-number", "links", "classification-cpv",
                "deadline-receipt", "value-eur", "notice-type", "contract-award"
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url, 
                    json=search_params, 
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        notices = data.get('notices', [])
                        
                        # Add search metadata
                        for notice in notices:
                            notice['_search_type'] = search_config['type']
                            notice['_search_group'] = search_config['group']
                            notice['_search_timestamp'] = datetime.now().isoformat()
                        
                        logger.info(f"Query returned {len(notices)} notices")
                        return notices
                    
                    elif response.status == 429:
                        logger.warning("Rate limit hit, backing off")
                        await asyncio.sleep(5)
                        return []
                    
                    else:
                        logger.error(f"API error: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Search execution error: {e}")
            return []
    
    def _remove_duplicates(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate notices by notice-identifier"""
        seen = set()
        unique_results = []
        
        for result in results:
            notice_id = result.get('notice-identifier', '')
            if notice_id and notice_id not in seen:
                seen.add(notice_id)
                unique_results.append(result)
        
        return unique_results
    
    async def _process_and_score_results(self, results: List[Dict], keywords: List[str],
                                       cpv_codes: List[str], countries: List[str],
                                       active_only: bool, min_value: int,
                                       include_documents: bool) -> List[Dict]:
        """Process and score all results"""
        processed_results = []
        
        for result in results:
            try:
                # Extract basic info
                tender_info = {
                    'notice_id': result.get('notice-identifier', ''),
                    'title': self._safe_get_text(result, 'notice-title'),
                    'buyer_name': self._safe_get_text(result, 'buyer-name'),
                    'country': result.get('buyer-country', ''),
                    'publication_date': result.get('publication-date', ''),
                    'deadline_date': result.get('deadline-receipt', ''),
                    'cpv_codes': self._extract_cpv_codes(result),
                    'notice_type': result.get('notice-type', ''),
                    'estimated_value_eur': self._extract_value(result),
                    'ted_url': self._generate_ted_url(result),
                    'search_metadata': {
                        'search_type': result.get('_search_type', ''),
                        'search_group': result.get('_search_group', []),
                        'found_timestamp': result.get('_search_timestamp', '')
                    }
                }
                
                # Add document links if requested
                if include_documents:
                    tender_info['document_links'] = self._extract_document_links(result)
                
                # Calculate relevance score
                relevance_score = self._calculate_relevance_score(
                    tender_info, keywords, cpv_codes, countries, min_value
                )
                tender_info['relevance_score'] = relevance_score
                
                # Determine tender status
                tender_info['status'] = self._determine_status(tender_info)
                
                # Apply filters
                if active_only and tender_info['status'] != 'active':
                    continue
                
                if min_value > 0 and tender_info['estimated_value_eur'] < min_value:
                    continue
                
                processed_results.append(tender_info)
                
            except Exception as e:
                logger.error(f"Error processing result: {e}")
                continue
        
        return processed_results
    
    def _safe_get_text(self, obj: Dict, field: str) -> str:
        """Safely extract text from multilingual fields"""
        try:
            value = obj.get(field, {})
            if isinstance(value, dict):
                # Try English first, then any available language
                return value.get('eng', value.get(list(value.keys())[0] if value else '', ''))
            elif isinstance(value, list) and value:
                if isinstance(value[0], dict):
                    return value[0].get('eng', str(value[0]))
                return str(value[0])
            return str(value) if value else ''
        except:
            return ''
    
    def _extract_cpv_codes(self, result: Dict) -> List[str]:
        """Extract CPV codes from result"""
        try:
            cpv_data = result.get('classification-cpv', [])
            if isinstance(cpv_data, list):
                return [str(cpv.get('cpv-code', '')) for cpv in cpv_data if cpv.get('cpv-code')]
            elif isinstance(cpv_data, dict):
                return [str(cpv_data.get('cpv-code', ''))] if cpv_data.get('cpv-code') else []
            return []
        except:
            return []
    
    def _extract_value(self, result: Dict) -> int:
        """Extract estimated contract value"""
        try:
            value_data = result.get('value-eur', 0)
            if isinstance(value_data, (int, float)):
                return int(value_data)
            elif isinstance(value_data, str):
                # Try to extract numeric value
                numeric_value = re.findall(r'[\d,]+', value_data.replace(',', ''))
                return int(''.join(numeric_value)) if numeric_value else 0
            return 0
        except:
            return 0
    
    def _generate_ted_url(self, result: Dict) -> str:
        """Generate TED URL for the tender"""
        try:
            # Try to get direct link first
            links = result.get('links', [])
            if links and isinstance(links, list):
                for link in links:
                    if isinstance(link, dict) and link.get('href'):
                        return link['href']
            
            # Fallback to publication number
            pub_number = result.get('publication-number', '')
            if pub_number:
                return f"https://ted.europa.eu/udl?uri=TED:NOTICE:{pub_number}:TEXT:EN:HTML"
            
            # Final fallback
            notice_id = result.get('notice-identifier', '')
            if notice_id:
                return f"https://ted.europa.eu/notices/{notice_id}"
            
            return ''
        except:
            return ''
    
    def _extract_document_links(self, result: Dict) -> List[Dict]:
        """Extract document links from result"""
        try:
            links = result.get('links', [])
            document_links = []
            
            if isinstance(links, list):
                for link in links:
                    if isinstance(link, dict):
                        link_info = {
                            'url': link.get('href', ''),
                            'type': link.get('type', 'document'),
                            'description': link.get('description', '')
                        }
                        if link_info['url']:
                            document_links.append(link_info)
            
            return document_links
        except:
            return []
    
    def _calculate_relevance_score(self, tender_info: Dict, keywords: List[str],
                                 cpv_codes: List[str], countries: List[str],
                                 min_value: int) -> int:
        """Calculate relevance score based on criteria"""
        score = 0
        title_lower = tender_info['title'].lower()
        buyer_lower = tender_info['buyer_name'].lower()
        tender_cpv = tender_info['cpv_codes']
        
        # Keyword matching (configurable weight)
        keyword_score = 0
        if keywords:
            keyword_matches = sum(1 for kw in keywords if kw.lower() in title_lower or kw.lower() in buyer_lower)
            keyword_score = min(100, (keyword_matches / len(keywords)) * 100)
        score += (keyword_score * self.scoring_criteria['keywordMatch'] / 100)
        
        # CPV code matching (configurable weight)
        cpv_score = 0
        if cpv_codes and tender_cpv:
            cpv_matches = sum(1 for cpv in cpv_codes if any(tcpv.startswith(cpv[:4]) for tcpv in tender_cpv))
            cpv_score = min(100, (cpv_matches / len(cpv_codes)) * 100)
        score += (cpv_score * self.scoring_criteria['cpvMatch'] / 100)
        
        # Country preference (configurable weight)
        country_score = 0
        if tender_info['country'] in countries:
            country_score = 100
        score += (country_score * self.scoring_criteria['countryMatch'] / 100)
        
        # Value matching (configurable weight)
        value_score = 0
        if tender_info['estimated_value_eur'] >= min_value:
            # Higher value tenders get higher scores
            if tender_info['estimated_value_eur'] > min_value * 10:
                value_score = 100
            elif tender_info['estimated_value_eur'] > min_value * 5:
                value_score = 75
            elif tender_info['estimated_value_eur'] > min_value:
                value_score = 50
        score += (value_score * self.scoring_criteria['valueMatch'] / 100)
        
        return min(100, int(score))
    
    def _determine_status(self, tender_info: Dict) -> str:
        """Determine if tender is active, expired, or awarded"""
        try:
            deadline_str = tender_info['deadline_date']
            if not deadline_str:
                return 'unknown'
            
            # Parse deadline date
            deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
            now = datetime.now(deadline.tzinfo)
            
            if now < deadline:
                return 'active'
            else:
                return 'expired'
                
        except:
            return 'unknown'