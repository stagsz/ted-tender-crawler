#!/usr/bin/env python3
"""
Test script to validate which CPV codes are supported by TED API
"""

import asyncio
import aiohttp
import json
from typing import List, Dict

async def test_cpv_code(cpv_code: str) -> Dict:
    """Test a single CPV code against TED API"""

    api_url = "https://api.ted.europa.eu/v3/notices/search"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "TED-CPV-Validator/1.0"
    }

    # Simple query with just the CPV code
    search_params = {
        "query": f'classification-cpv="{cpv_code}"',
        "limit": 1,
        "fields": ["notice-identifier", "publication-number"]
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                api_url,
                json=search_params,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:

                status = response.status

                if status == 200:
                    data = await response.json()
                    count = len(data.get('notices', []))
                    return {
                        'cpv_code': cpv_code,
                        'status': 'VALID',
                        'http_status': 200,
                        'results': count,
                        'message': f'✅ Valid - Found {count} tenders'
                    }
                else:
                    error_text = await response.text()
                    return {
                        'cpv_code': cpv_code,
                        'status': 'INVALID',
                        'http_status': status,
                        'results': 0,
                        'message': f'❌ API Error: {error_text[:200]}'
                    }

    except Exception as e:
        return {
            'cpv_code': cpv_code,
            'status': 'ERROR',
            'http_status': 0,
            'results': 0,
            'message': f'⚠️ Exception: {str(e)[:200]}'
        }

async def test_all_cpv_codes(cpv_codes: List[str]):
    """Test all CPV codes with rate limiting"""

    print("=" * 80)
    print("TED API CPV Code Validation Test")
    print("=" * 80)
    print(f"\nTesting {len(cpv_codes)} CPV codes...\n")

    results = []

    for i, cpv_code in enumerate(cpv_codes, 1):
        print(f"[{i}/{len(cpv_codes)}] Testing CPV code: {cpv_code}...", end=" ")

        result = await test_cpv_code(cpv_code)
        results.append(result)

        print(result['message'])

        # Rate limiting - wait 1 second between requests
        if i < len(cpv_codes):
            await asyncio.sleep(1)

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    valid_codes = [r for r in results if r['status'] == 'VALID']
    invalid_codes = [r for r in results if r['status'] == 'INVALID']
    error_codes = [r for r in results if r['status'] == 'ERROR']

    print(f"\n✅ Valid codes: {len(valid_codes)}/{len(cpv_codes)}")
    print(f"❌ Invalid codes: {len(invalid_codes)}/{len(cpv_codes)}")
    print(f"⚠️ Errors: {len(error_codes)}/{len(cpv_codes)}")

    if invalid_codes:
        print("\n🔴 INVALID CPV CODES (Not supported by TED API):")
        for result in invalid_codes:
            print(f"  - {result['cpv_code']}")

    if valid_codes:
        print("\n✅ VALID CPV CODES (Supported by TED API):")
        for result in valid_codes:
            print(f"  - {result['cpv_code']} ({result['results']} tenders found)")

    # Save detailed results
    with open('cpv_validation_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n📄 Detailed results saved to: cpv_validation_results.json")

if __name__ == '__main__':
    # Your CPV codes from the configuration
    cpv_codes_to_test = [
        "09320000", "09323000", "09324000",
        "42000000", "42160000", "42161000", "42163000", "42996700",
        "42510000", "42515000",
        "90712500", "90715200",
        "42310000",
        "45252300", "45232140",
        "90513300",
        "42122000", "71320000"
    ]

    # Also test recommended division-level alternatives
    print("\n" + "=" * 80)
    print("PART 1: Testing your original CPV codes")
    print("=" * 80)
    asyncio.run(test_all_cpv_codes(cpv_codes_to_test))

    print("\n\n" + "=" * 80)
    print("PART 2: Testing recommended division-level codes")
    print("=" * 80)

    recommended_codes = [
        "09000000",  # Petroleum products
        "42000000",  # Industrial machinery
        "45000000",  # Construction work
        "90000000",  # Sewage, refuse, cleaning
        "90700000",  # Environmental services
        "71000000"   # Architectural, engineering
    ]

    asyncio.run(test_all_cpv_codes(recommended_codes))
