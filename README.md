# TED.EU Tender Search & Monitor

🇪🇺 **Automated European Public Procurement Monitoring**

Search and monitor European public procurement tenders from TED.EU (Tenders Electronic Daily) with customizable filtering, intelligent relevance scoring, and multi-format outputs. Perfect for businesses, consultants, and researchers tracking EU opportunities.

## 🚀 Features

- **🔍 Flexible Search**: Custom keywords, CPV codes, countries, and date ranges
- **📊 Smart Scoring**: Configurable relevance scoring based on your criteria  
- **🏭 Industry Templates**: Pre-configured searches for common sectors
- **⚡ Real-time Data**: Direct API access to TED.EU database
- **📈 Active Filtering**: Only show tenders still open for submission
- **💰 Value Filtering**: Filter by minimum contract values
- **🔗 Document Links**: Access to official tender documents
- **📋 Multiple Formats**: JSON, CSV, Excel outputs

## 💼 Perfect For

- **Consulting Firms** seeking government contracts
- **SME Businesses** expanding into EU markets  
- **Research Organizations** studying procurement trends
- **Business Intelligence** companies needing raw data feeds
- **Legal Firms** tracking opportunities for clients
- **Startups** seeking government contracts

## 📋 Input Configuration

### Basic Settings
```json
{
  "searchKeywords": ["software development", "IT consulting"],
  "countries": ["DE", "FR", "IT"],
  "yearFrom": 2024,
  "yearTo": 2024,
  "maxResults": 100
}
```

### Advanced Configuration
```json
{
  "searchKeywords": ["cloud services", "digital transformation"],
  "cpvCodes": ["72000000", "72200000"],
  "countries": ["DE", "FR", "IT", "ES", "NL"],
  "yearFrom": 2024,
  "yearTo": 2024,
  "activeOnly": true,
  "minValue": 50000,
  "maxResults": 200,
  "industryTemplate": "it-software",
  "scoringCriteria": {
    "keywordMatch": 50,
    "cpvMatch": 30,
    "countryMatch": 15,
    "valueMatch": 5
  }
}
```

## 🏭 Industry Templates

Pre-configured keyword and CPV code sets for common industries:

| Template | Description | Example Keywords |
|----------|-------------|------------------|
| `it-software` | IT services, software development | software development, cloud services, cybersecurity |
| `construction` | Building, infrastructure, civil engineering | construction, building, renovation, infrastructure |
| `healthcare` | Medical equipment, healthcare services | medical equipment, healthcare, pharmaceutical |
| `consulting` | Management and business consulting | consulting services, strategic planning, advisory |
| `engineering` | Technical and engineering services | engineering services, technical consulting, design |
| `environmental` | Environmental and sustainability services | environmental services, waste management, sustainability |
| `education` | Educational services and training | educational services, training, e-learning |
| `transportation` | Transport and logistics services | transportation, logistics, fleet management |
| `energy` | Energy and utilities services | renewable energy, energy efficiency, power generation |

## 📊 Output Format

Each tender includes:

```json
{
  "notice_id": "123456-2024",
  "title": "IT Infrastructure Modernization",
  "buyer_name": "Ministry of Digital Affairs",
  "country": "DE",
  "publication_date": "2024-01-15",
  "deadline_date": "2024-02-15",
  "estimated_value_eur": 250000,
  "cpv_codes": ["72000000", "72200000"],
  "relevance_score": 85,
  "status": "active",
  "ted_url": "https://ted.europa.eu/udl?uri=TED:NOTICE:...",
  "document_links": [
    {
      "url": "https://...",
      "type": "specification",
      "description": "Technical requirements"
    }
  ]
}
```

## 🎯 Relevance Scoring

Smart scoring algorithm considers:

- **Keyword Match** (40%): How well keywords match tender title/description
- **CPV Code Match** (30%): Alignment with specified procurement categories  
- **Country Preference** (20%): Preference for selected countries
- **Contract Value** (10%): Higher value contracts score higher

Scores range from 0-100, with 70+ indicating high relevance.

## 📈 Usage Examples

### Find IT Consulting Opportunities in Germany
```json
{
  "industryTemplate": "it-software",
  "countries": ["DE"],
  "minValue": 100000,
  "activeOnly": true
}
```

### Monitor Construction Projects in EU
```json
{
  "industryTemplate": "construction", 
  "countries": ["DE", "FR", "IT", "ES", "NL"],
  "yearFrom": 2024,
  "yearTo": 2024
}
```

### Custom Healthcare Equipment Search
```json
{
  "searchKeywords": ["medical devices", "diagnostic equipment", "hospital equipment"],
  "cpvCodes": ["33100000", "33600000"],
  "countries": ["DE", "AT", "CH"],
  "minValue": 50000
}
```

## 🔧 Technical Details

- **Data Source**: TED.EU official API
- **Update Frequency**: Real-time API access
- **Rate Limiting**: Automatic throttling to respect API limits
- **Deduplication**: Automatic removal of duplicate notices
- **Error Handling**: Robust error recovery and logging

## 💡 Pro Tips

1. **Use Industry Templates** for quick setup with proven keyword sets
2. **Combine Keywords + CPV** for best coverage and relevance
3. **Set Minimum Values** to focus on substantial opportunities
4. **Enable Active Only** to avoid expired tenders
5. **Adjust Scoring Weights** based on your priorities

## 📞 Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive guides and examples
- **Community**: Join other users sharing best practices

## 🏆 Success Stories

> *"Found 3 major consulting contracts worth €2M+ in first month using TED Actor"*  
> — Management Consulting Firm

> *"Reduced tender research time from 2 days to 30 minutes per week"*  
> — IT Services Company  

> *"Discovered opportunities in new EU markets we never considered"*  
> — Engineering Startup

---

**Start monitoring European procurement opportunities today!** 🇪🇺

*Built with ❤️ for the European business community*