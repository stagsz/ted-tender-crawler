#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TED SPIG-GMAB Customized Tender Monitor - Cooling Systems & Air Pollution Control
Enhanced version focused on cooling systems and air pollution control opportunities
Customized for SPIG-GMAB's expertise in water conservation and environmental solutions

VERSION: 3.0 - SPIG-GMAB SPECIALIZED SEARCH
- Focus on cooling systems, air pollution control, and environmental technologies
- Targets industrial facilities, power generation, and manufacturing sectors
- Includes aftermarket upgrades, replacement parts, and system monitoring opportunities
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TedSPIGGMABMonitor:
    """TED Monitor Customized for SPIG-GMAB - Cooling Systems & Air Pollution Control"""
    
    def __init__(self):
        self.api_url = "https://api.ted.europa.eu/v3/notices/search"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Industries relevant for SPIG-GMAB's cooling systems & air pollution control
        self.tier1_operators = [
            # Major Industrial Manufacturing
            "Siemens", "ABB", "General Electric", "Schneider Electric", "Emerson",
            "Honeywell", "Johnson Controls", "Danfoss", "Grundfos", "Wilo",
            "Alfa Laval", "GEA Group", "Kelvion", "SPX Technologies", "Tranter",
            
            # Chemical & Petrochemical
            "BASF", "Bayer", "Evonik", "Covestro", "Lanxess", "Wacker Chemie",
            "Shell", "BP", "Total", "ExxonMobil", "Chevron", "ENI", "Repsol",
            "SABIC", "Dow Chemical", "DuPont", "3M", "Huntsman",
            
            # Steel & Metal Processing
            "ThyssenKrupp", "ArcelorMittal", "Salzgitter", "Voestalpine", "SSAB",
            "Outokumpu", "Norsk Hydro", "Alcoa", "Rio Tinto", "BHP",
            
            # Food & Beverage Processing
            "Nestle", "Unilever", "Danone", "Carlsberg", "Heineken", "AB InBev",
            "Coca-Cola", "PepsiCo", "Kraft Heinz", "Mondelez",
            
            # Pharmaceutical & Healthcare
            "Roche", "Novartis", "Sanofi", "Pfizer", "Merck", "Johnson & Johnson",
            "GSK", "AstraZeneca", "Boehringer Ingelheim", "Bayer Healthcare",
            
            # Automotive Manufacturing
            "Volkswagen", "BMW", "Mercedes-Benz", "Audi", "Porsche", "Opel",
            "Ford", "General Motors", "Stellantis", "Toyota", "Honda",
            
            # Data Centers & IT Infrastructure
            "Microsoft", "Google", "Amazon", "Meta", "Apple", "IBM", "Oracle",
            "SAP", "Equinix", "Digital Realty", "CoreSite", "Interxion"
        ]
        
        self.tier2_operators = [
            # Regional Industrial Companies
            "Bosch", "Continental", "Schaeffler", "ZF Friedrichshafen", "Mahle",
            "Knorr-Bremse", "Rheinmetall", "MTU Aero Engines", "MAN Energy",
            
            # Mining & Materials
            "Heidelberg Cement", "Holcim", "LafargeHolcim", "CRH", "Cemex",
            "Saint-Gobain", "Owens Corning", "Johns Manville",
            
            # Paper & Pulp
            "UPM", "Stora Enso", "Smurfit Kappa", "Mondi", "International Paper",
            "Sappi", "Sodra", "Metsa Group",
            
            # Textile & Consumer Goods
            "Adidas", "PUMA", "Hugo Boss", "Zalando", "H&M", "Inditex",
            "LVMH", "Kering", "Richemont", "Swatch Group",
            
            # Healthcare Facilities & Hospitals
            "Charite", "Universitatsklinikum", "Helios", "Asklepios", "Rhon-Klinikum",
            "Fresenius", "B. Braun", "Drager", "Siemens Healthineers",
            
            # Municipal & Government
            "Stadt Munchen", "Stadt Berlin", "Stadt Hamburg", "Stadt Koln",
            "Stadt Frankfurt", "Vienna", "Amsterdam", "Brussels", "Copenhagen"
        ]
        
        # SPIG-GMAB specialized keywords - Cooling Systems & Air Pollution Control
        self.spig_keywords = [
            # Cooling Systems (Core expertise)
            "cooling system", "cooling tower", "air cooler", "water cooler", "chiller",
            "heat exchanger", "condenser", "evaporator", "cooling circuit", "cooling loop",
            "cooling infrastructure", "industrial cooling", "process cooling", "HVAC",
            "cooling equipment", "cooling technology", "cooling solution", "cooling upgrade",
            
            # Air Pollution Control (Core expertise)
            "air pollution control", "emission control", "air treatment", "air cleaning",
            "air filtration", "dust control", "particulate control", "gas cleaning",
            "pollution abatement", "environmental control", "emission reduction",
            "air quality", "atmospheric protection", "exhaust treatment",
            
            # Water Conservation (Core expertise)
            "water conservation", "water treatment", "water recycling", "water management",
            "water saving", "water efficiency", "water reuse", "water recovery",
            "wastewater treatment", "water purification", "water system",
            
            # Aftermarket & Maintenance (Service area)
            "aftermarket", "replacement parts", "spare parts", "maintenance", "retrofit",
            "upgrade", "modernization", "refurbishment", "overhaul", "repair",
            "system monitoring", "control system", "automation", "instrumentation",
            
            # Industrial Applications
            "power plant", "manufacturing", "industrial facility", "process plant",
            "chemical plant", "petrochemical", "refinery", "steel plant", "cement plant",
            "thermal power", "combined cycle", "cogeneration", "waste-to-energy"
        ]
        
        # SPIG-GMAB relevant CPV codes
        self.spig_cpv_codes = [
            # Air Pollution Control
            "42514000",  # Air pollution control equipment
            "42514200",  # Dust collection equipment  
            "42514300",  # Gas cleaning equipment
            "42997200",  # Emission control equipment
            "42997300",  # Pollution monitoring equipment
            
            # Cooling & HVAC Systems
            "42500000",  # Air-conditioning, refrigeration and ventilation equipment
            "42510000",  # Air-conditioning equipment
            "42520000",  # Refrigeration equipment
            "42530000",  # Ventilation equipment
            "42900000",  # Industrial machinery
            "42910000",  # Heat exchangers
            "42997100",  # Cooling systems
            
            # Water Treatment & Conservation
            "42411000",  # Water-treatment equipment
            "42412000",  # Water-purification equipment
            "42413000",  # Water-distribution equipment
            "42700000",  # Water-supply equipment
            "42997000",  # Environmental control equipment
            
            # Maintenance & Aftermarket
            "50000000",  # Repair and maintenance services
            "50700000",  # Repair and maintenance services of building installations
            "50800000",  # Miscellaneous repair and maintenance services
            "34000000",  # Transport equipment and auxiliary products to transportation
            "42000000",  # Industrial machinery
        ]

    def search_by_operator(self, operator, limit=100, days_back=90):
        """Search tenders by operator name with date filter"""
        # Try different query variations for better results
        queries = [
            f'buyer-name = "{operator}"',
            f'notice-title = "{operator}"',
        ]
        
        all_notices = []
        
        for query_template in queries:
            query = {
                "query": query_template,
                "limit": limit,
                "fields": ["notice-identifier", "notice-title", "buyer-name", "publication-date", "publication-number", "links", "classification-cpv"]
            }
            
            logger.info(f"Searching operator: {operator} with query: {query_template}")
            
            try:
                response = requests.post(self.api_url, json=query, headers=self.headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    notices = data.get('notices', [])
                    logger.info(f"Found {len(notices)} tenders for {operator}")
                    
                    # Add search metadata
                    for notice in notices:
                        notice['search_operator'] = operator
                        notice['search_type'] = 'operator_search'
                    
                    all_notices.extend(notices)
                elif response.status_code == 429:
                    logger.warning(f"Rate limit hit for {operator}, skipping additional queries")
                    break
                else:
                    logger.error(f"API error for {operator}: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Exception searching {operator}: {e}")
                
        # Remove duplicates based on notice-identifier
        unique_notices = {}
        for notice in all_notices:
            notice_id = notice.get('notice-identifier', '')
            if notice_id and notice_id not in unique_notices:
                unique_notices[notice_id] = notice
        
        return list(unique_notices.values())

    def search_by_operator_tier(self, operators_list, tier_name):
        """Search all operators in a tier"""
        tier_results = []
        
        logger.info(f"Searching {tier_name} operators: {len(operators_list)} operators")
        
        for operator in operators_list:
            operator_results = self.search_by_operator(operator)
            tier_results.extend(operator_results)
            
        logger.info(f"{tier_name} total results: {len(tier_results)}")
        return tier_results

    def validate_spig_relevance(self, tender_info):
        """Validate if tender is SPIG-GMAB relevant and calculate enhanced scoring"""
        score = 0
        title_lower = str(tender_info.get('title', '')).lower()
        buyer_lower = str(tender_info.get('buyer_name', '')).lower()
        cpv_codes = str(tender_info.get('cpv_codes', '')).lower()
        
        # Core SPIG-GMAB expertise areas (30 points each)
        cooling_keywords = ['cooling system', 'cooling tower', 'heat exchanger', 'chiller', 'condenser', 'cooling']
        for keyword in cooling_keywords:
            if keyword in title_lower:
                score += 30
                break
        
        # Air pollution control (25 points each)
        air_control_keywords = ['air pollution control', 'emission control', 'air treatment', 'air cleaning', 'air filtration']
        for keyword in air_control_keywords:
            if keyword in title_lower:
                score += 25
                break
        
        # Water conservation (25 points each)
        water_keywords = ['water conservation', 'water treatment', 'water recycling', 'water management', 'wastewater']
        for keyword in water_keywords:
            if keyword in title_lower:
                score += 25
                break
        
        # Aftermarket & services (20 points each)
        service_keywords = ['aftermarket', 'replacement parts', 'spare parts', 'maintenance', 'retrofit', 'upgrade']
        for keyword in service_keywords:
            if keyword in title_lower:
                score += 20
                break
        
        # Industrial applications (15 points each)
        industrial_keywords = ['power plant', 'manufacturing', 'industrial facility', 'process plant', 'chemical plant']
        for keyword in industrial_keywords:
            if keyword in title_lower:
                score += 15
                break
        
        # Environmental systems (12 points each)
        env_keywords = ['environmental', 'pollution', 'emission', 'environmental control']
        for keyword in env_keywords:
            if keyword in title_lower:
                score += 12
                break
        
        # SPIG-GMAB relevant CPV codes (20 points)
        for cpv in self.spig_cpv_codes:
            if cpv in cpv_codes:
                score += 20
                break
        
        # Operator-based search gets base score (15 points)
        if tender_info.get('search_type') == 'operator_search':
            score += 15
        
        # Tier 1 operator bonus (10 points)
        if tender_info.get('search_operator') in self.tier1_operators:
            score += 10
        
        return min(score, 100)  # Cap at 100

    def execute_operator_first_search(self):
        """Execute the improved operator-first search strategy"""
        all_results = []
        
        print("Executing Operator-First Search Strategy")
        print("=" * 60)
        
        # Tier 1: Major industrial operators (highest priority)
        print("Tier 1: Searching major industrial operators...")
        tier1_results = self.search_by_operator_tier(self.tier1_operators, "Tier 1")
        all_results.extend(tier1_results)
        
        # Tier 2: Additional operators
        print("Tier 2: Searching additional operators...")
        tier2_results = self.search_by_operator_tier(self.tier2_operators, "Tier 2")
        all_results.extend(tier2_results)
        
        return all_results

    def process_and_score_results(self, raw_results):
        """Process results and apply SPIG-GMAB relevance scoring"""
        processed_results = []
        
        logger.info(f"Processing {len(raw_results)} raw results...")
        
        for result in raw_results:
            try:
                # Extract and clean data
                tender_info = {
                    'notice_id': result.get('notice-identifier', ''),
                    'title': self.safe_get_text(result, 'notice-title'),
                    'buyer_name': self.safe_get_text(result, 'buyer-name'),
                    'publication_date': result.get('publication-date', ''),
                    'publication_number': result.get('publication-number', ''),
                    'cpv_codes': str(result.get('classification-cpv', '')),
                    'search_operator': result.get('search_operator', ''),
                    'search_type': result.get('search_type', ''),
                    'ted_url': self.generate_ted_url(result),
                }
                
                # Calculate SPIG-GMAB relevance score
                spig_score = self.validate_spig_relevance(tender_info)
                tender_info['spig_relevance_score'] = spig_score
                
                # Categorize tender type
                tender_info['spig_category'] = self.categorize_spig_type(tender_info)
                
                # Only include if SPIG-relevant (score >= 10)
                if spig_score >= 10:
                    processed_results.append(tender_info)
                
            except Exception as e:
                logger.error(f"Error processing result: {e}")
                continue
        
        # Sort by SPIG relevance score
        processed_results.sort(key=lambda x: x['spig_relevance_score'], reverse=True)
        
        logger.info(f"Filtered to {len(processed_results)} SPIG-GMAB relevant tenders")
        return processed_results

    def safe_get_text(self, obj, field):
        """Safely extract text from multilingual fields"""
        try:
            value = obj.get(field, {})
            if isinstance(value, dict):
                return value.get('eng', value.get(list(value.keys())[0] if value else '', ''))
            elif isinstance(value, list) and value:
                if isinstance(value[0], dict):
                    return value[0].get('eng', str(value[0]))
                return str(value[0])
            return str(value) if value else ''
        except:
            return ''

    def generate_ted_url(self, tender):
        """Generate TED URL"""
        try:
            links = tender.get('links', [])
            if links and isinstance(links, list):
                return links[0].get('href', '')
            
            pub_number = tender.get('publication-number', '')
            if pub_number:
                return f"https://ted.europa.eu/udl?uri=TED:NOTICE:{pub_number}:TEXT:EN:HTML"
            
            return ''
        except:
            return ''

    def categorize_spig_type(self, tender_info):
        """Categorize SPIG-GMAB opportunity type"""
        title_lower = str(tender_info['title']).lower()
        
        if any(term in title_lower for term in ['cooling system', 'cooling tower', 'heat exchanger', 'chiller']):
            return 'Cooling Systems'
        elif any(term in title_lower for term in ['air pollution control', 'emission control', 'air treatment']):
            return 'Air Pollution Control'
        elif any(term in title_lower for term in ['water conservation', 'water treatment', 'water recycling']):
            return 'Water Conservation'
        elif any(term in title_lower for term in ['aftermarket', 'replacement parts', 'spare parts', 'maintenance']):
            return 'Aftermarket/Maintenance'
        elif any(term in title_lower for term in ['hvac', 'air conditioning', 'ventilation']):
            return 'HVAC Systems'
        elif any(term in title_lower for term in ['retrofit', 'upgrade', 'modernization']):
            return 'Upgrades/Retrofits'
        elif any(term in title_lower for term in ['monitoring', 'control system', 'automation']):
            return 'System Monitoring/Controls'
        elif any(term in title_lower for term in ['environmental', 'pollution', 'emission']):
            return 'Environmental Solutions'
        else:
            return 'Industrial/General'

    def save_results(self, tenders):
        """Save results with enhanced formatting"""
        if not tenders:
            logger.warning("No tenders to save")
            return None
        
        # Create DataFrame
        df = pd.DataFrame(tenders)
        
        # Generate filenames with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        csv_filename = f"ted_spig_gmab_{timestamp}.csv"
        xlsx_filename = f"ted_spig_gmab_{timestamp}.xlsx"
        
        csv_path = os.path.join(r"C:\Users\staff\anthropicFun\Adiox\tedcpv\results", csv_filename)
        xlsx_path = os.path.join(r"C:\Users\staff\anthropicFun\Adiox\tedcpv\results", xlsx_filename)
        
        # Ensure results directory exists
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        # Save files
        df.to_csv(csv_path, index=False)
        df.to_excel(xlsx_path, index=False)
        
        logger.info(f"Results saved to: {xlsx_path}")
        return xlsx_path

def main():
    """Main execution with SPIG-GMAB customized search strategy"""
    print("TED SPIG-GMAB Tender Monitor - CUSTOMIZED VERSION")
    print("NO API KEY REQUIRED - Uses Public TED API")
    print("Cooling Systems & Air Pollution Control Focus")
    print("=" * 70)
    
    monitor = TedSPIGGMABMonitor()
    
    print(f"Tier 1 Operators: {len(monitor.tier1_operators)}")
    print(f"Tier 2 Operators: {len(monitor.tier2_operators)}")
    print(f"SPIG Keywords: {len(monitor.spig_keywords)}")
    print(f"SPIG CPV Codes: {len(monitor.spig_cpv_codes)}")
    print()
    
    # Execute operator-first search
    raw_results = monitor.execute_operator_first_search()
    
    if not raw_results:
        print("No results found")
        return
    
    print(f"Raw results found: {len(raw_results)}")
    
    # Process and score for SPIG-GMAB relevance
    spig_relevant_tenders = monitor.process_and_score_results(raw_results)
    
    if not spig_relevant_tenders:
        print("No SPIG-GMAB relevant tenders found")
        return
    
    print(f"SPIG-GMAB relevant tenders: {len(spig_relevant_tenders)}")
    
    # Analyze results by score
    high_relevance = [t for t in spig_relevant_tenders if t['spig_relevance_score'] >= 50]
    medium_relevance = [t for t in spig_relevant_tenders if 30 <= t['spig_relevance_score'] < 50]
    low_relevance = [t for t in spig_relevant_tenders if 10 <= t['spig_relevance_score'] < 30]
    
    print(f"High relevance (50+): {len(high_relevance)}")
    print(f"Medium relevance (30-49): {len(medium_relevance)}")
    print(f"Low relevance (10-29): {len(low_relevance)}")
    
    # Show top results
    if high_relevance:
        print("\nTop High Relevance SPIG-GMAB Opportunities:")
        for i, tender in enumerate(high_relevance[:5], 1):
            print(f"{i}. {tender['title'][:80]}...")
            print(f"   Operator: {tender['search_operator']}")
            print(f"   Buyer: {tender['buyer_name'][:50]}")
            print(f"   SPIG Score: {tender['spig_relevance_score']}")
            print(f"   Category: {tender['spig_category']}")
            print(f"   URL: {tender['ted_url']}")
            print()
    
    # Save results
    output_file = monitor.save_results(spig_relevant_tenders)
    if output_file:
        print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    main()