# 🇪🇺 TED Tender Crawler - European Public Procurement Search Engine

**Discover and track European public procurement opportunities with intelligent filtering and industry-specific templates**

## 🎯 What This Actor Does

Search Europe's official TED database for public procurement opportunities. Find relevant tenders across all EU countries with smart filtering, industry templates, and intelligent scoring to match your business needs.

## ✨ Key Features

### 🔍 **Smart Search Capabilities**
- **Keyword-based search** across tender titles and descriptions
- **CPV code filtering** for precise procurement category targeting
- **Multi-country support** with all EU member states
- **Date range filtering** for recent or historical tenders
- **Contract value filtering** to match your business size

### 🏭 **Industry Templates** 
Pre-configured keyword and CPV code sets for instant setup:
- 💻 **IT & Software** - Cloud services, development, cybersecurity
- 🏗️ **Construction** - Building, infrastructure, civil engineering
- 🏥 **Healthcare** - Medical equipment, pharmaceuticals, hospital services
- 💼 **Consulting** - Management, business advisory, strategic planning
- ⚙️ **Engineering** - Technical consulting, system design, project engineering
- 🌿 **Environmental** - Waste management, renewable energy, sustainability
- 🎓 **Education** - Training services, e-learning, curriculum development
- 🚛 **Transportation** - Logistics, fleet management, public transport
- ⚡ **Energy** - Power generation, smart grid, energy efficiency

### 🎯 **Intelligent Relevance Scoring**
Customizable scoring algorithm that ranks tenders based on:
- **Keyword matching** (40% default weight)
- **CPV code alignment** (30% default weight)  
- **Country preference** (20% default weight)
- **Contract value fit** (10% default weight)

### 📊 **Rich Data Output**
Each tender result includes:
- Complete tender details and buyer information
- Publication and deadline dates
- Estimated contract value in EUR
- CPV classification codes
- Direct links to official TED pages
- Document download links
- Tender status (active/expired)
- Custom relevance score

## 🚀 Perfect For

- **🏢 Businesses** seeking European procurement opportunities
- **👔 Consultants** tracking relevant tender calls
- **📈 Market researchers** analyzing procurement trends
- **🏛️ Government contractors** expanding into EU markets
- **💼 Sales teams** identifying potential clients
- **📊 Business intelligence** gathering competitive insights

## ⚙️ Easy Configuration

### Quick Start Options:
1. **Choose an industry template** for instant setup
2. **Add your keywords** for custom searches  
3. **Select target countries** from EU member states
4. **Set date ranges** and contract value filters
5. **Customize scoring weights** for optimal relevance

### Advanced Features:
- **Active-only filtering** for open tenders
- **Flexible output formats** (JSON, CSV, Excel)
- **Document link inclusion** for full tender packages
- **Batch processing** with rate limiting
- **Comprehensive logging** for monitoring

## 📈 Sample Use Cases

**IT Company Example:**
```json
{
  "industryTemplate": "it-software",
  "countries": ["DE", "FR", "NL"],
  "minValue": 50000,
  "activeOnly": true
}
```

**Construction Firm Example:**
```json
{
  "industryTemplate": "construction", 
  "searchKeywords": ["road construction", "bridge repair"],
  "countries": ["IT", "ES", "PT"],
  "maxResults": 200
}
```

## 🔧 Technical Excellence

- **🚀 High Performance** - Async processing with intelligent rate limiting
- **📡 API v3 Integration** - Uses latest TED.europa.eu API
- **🛡️ Robust Error Handling** - Graceful failure recovery
- **📊 Progress Tracking** - Real-time processing updates
- **🔄 Deduplication** - Automatic removal of duplicate entries
- **⚡ Optimized Queries** - Smart query building for maximum coverage

## 💡 Why Choose This Actor?

1. **🎯 Precision** - Industry templates eliminate noise and find relevant opportunities
2. **⏱️ Time-Saving** - Automated search across 27 EU countries simultaneously  
3. **🧠 Intelligence** - Smart relevance scoring puts best matches first
4. **🔧 Flexibility** - Fully customizable for any industry or use case
5. **📊 Comprehensive** - Rich data output with all essential tender information
6. **🚀 Reliable** - Professional-grade code with comprehensive testing

## 🎉 Get Started

Simply select your industry template, choose your target countries, and let the crawler find your next business opportunity in Europe's €2 trillion public procurement market!

---

**🏆 Built with Apify's robust infrastructure for reliable, scalable tender discovery**

---

This description positions your TED Tender Crawler as a professional, feature-rich solution that solves real business problems while highlighting its technical excellence and ease of use.