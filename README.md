# TTEdb: Target Trial Emulation Database

[![Live Demo](https://img.shields.io/badge/Live%20Demo-ttedb.xeradb.com-blue?style=for-the-badge)](https://ttedb.xeradb.com)
[![Django](https://img.shields.io/badge/Django-4.2+-green?style=flat-square)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

A comprehensive database and meta-analysis platform for Target Trial Emulation (TTE) studies, designed to advance causal inference research in epidemiology and clinical research.

## 🎯 **Purpose**

TTEdb serves as the first systematic repository of Target Trial Emulation studies worldwide, enabling researchers to:

- **Explore** the growing landscape of TTE methodology applications
- **Compare** TTE results with their corresponding Randomized Controlled Trials (RCTs)
- **Analyze** patterns of concordance and discordance between study designs
- **Assess** research transparency and methodological rigor in causal inference
- **Learn** from comprehensive educational resources and best practices

## 🚀 **Key Features**

### 📊 **Comprehensive Analysis Platform**
- **Bayesian Meta-Analysis**: Stratified analysis by effect measure type (HR, OR, RR, MD, SMD)
- **Publication Bias Detection**: Funnel plots, outlier detection, and inlier analysis
- **Research Transparency Assessment**: Protocol registration, data sharing, and funding analysis
- **Interactive Visualizations**: Forest plots, concordance analysis, and temporal trends

### 🔍 **Study Database**
- **TTE Studies Repository**: Systematic collection of Target Trial Emulation studies
- **RCT Comparisons**: Direct comparisons between TTE and RCT results
- **PICO Elements**: Detailed Population, Intervention, Comparison, Outcome data
- **Effect Estimates**: Comprehensive collection of study results and confidence intervals

### 📚 **Learning Hub**
- **Educational Resources**: Curated collection of TTE methodology papers, tutorials, and guidelines
- **Best Practices**: Evidence-based recommendations for TTE study design and reporting
- **Interactive Examples**: Real-world case studies demonstrating TTE applications

### 🛠 **Research Tools**
- **Advanced Search**: Multi-faceted filtering by disease, intervention, outcome, methodology
- **Data Export**: Download study data for meta-analysis and systematic reviews
- **API Access**: Programmatic access to database for automated analysis
- **Visualization Tools**: Interactive charts and plots for data exploration

## 🌐 **Live Demo**

Explore TTEdb at: **[https://ttedb.xeradb.com](https://ttedb.xeradb.com)**

### Navigation Overview:
- **Home**: Database overview and quick access to key features
- **TTE Studies**: Browse and search the complete study database
- **TTE vs RCT**: Compare Target Trial Emulation and RCT results
- **Analysis**: Comprehensive meta-analysis and research quality assessment
- **Learning Hub**: Educational resources and methodology guides
- **API**: Programmatic access documentation

## 📈 **Analysis Capabilities**

### **Descriptive Analysis**
- Publication patterns and methodological evolution over time
- Geographic distribution of TTE research
- Disease category and intervention type analysis
- Sample size distributions and data source characteristics

### **Primary Analysis**
- **Bayesian Meta-Analysis**: Effect estimate pooling by measure type
- **Forest Plots**: Visual representation of study effects and confidence intervals
- **Funnel Plot Analysis**: Publication bias and small-study effects detection
- **Concordance Assessment**: TTE-RCT agreement across multiple dimensions

### **Secondary Analysis**
- **Subgroup Analysis**: By disease category, sample size, methodology rigor
- **Sensitivity Analysis**: Robustness testing with different statistical approaches
- **Temporal Trends**: Evolution of concordance patterns over time
- **Methodology Impact**: Effect of DAGs, protocols, and transparency on outcomes

### **Research Transparency**
- Protocol registration patterns and trends
- Data and code availability assessment
- Funding source analysis and conflict of interest patterns
- Composite transparency scoring system

## 🛠 **Installation & Setup**

### **Prerequisites**
- Python 3.8+
- Django 4.2+
- PostgreSQL (recommended) or SQLite
- Node.js (for frontend dependencies)

### **Local Development Setup**

1. **Clone the repository**
```bash
git clone https://github.com/choxos/TTEdb.git
cd TTEdb
```

2. **Create virtual environment**
```bash
python -m venv ttedb_env
source ttedb_env/bin/activate  # On Windows: ttedb_env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment configuration**
```bash
cp .env.example .env
# Edit .env with your database settings and secret key
```

5. **Database setup**
```bash
python manage.py migrate
python manage.py populate_learning_resources  # Load sample data
```

6. **Run development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access TTEdb locally.

### **Production Deployment**

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed production deployment instructions including:
- Server configuration (Ubuntu/Nginx/Gunicorn)
- SSL certificate setup
- Database optimization
- Static file serving
- Monitoring and logging

## 📖 **Usage Guide**

### **For Researchers**

1. **Browse Studies**: Use the TTE Studies section to explore the database
2. **Compare Results**: Visit TTE vs RCT to examine study concordance
3. **Conduct Analysis**: Use the Analysis section for meta-analysis and bias assessment
4. **Access Data**: Download study data or use the API for programmatic access

### **For Methodologists**

1. **Assess Trends**: Analyze methodological evolution in TTE research
2. **Quality Assessment**: Evaluate research transparency and rigor patterns
3. **Publication Bias**: Use funnel plots and outlier detection tools
4. **Best Practices**: Contribute to and learn from the Learning Hub

### **For Educators**

1. **Teaching Materials**: Access curated resources in the Learning Hub
2. **Case Studies**: Use real TTE examples for methodology training
3. **Interactive Examples**: Demonstrate causal inference concepts with live data

## 🔌 **API Documentation**

TTEdb provides a RESTful API for programmatic access to study data.

### **Base URL**: `https://ttedb.xeradb.com/api/`

### **Key Endpoints**:

- `GET /api/studies/` - List all TTE studies
- `GET /api/studies/{id}/` - Retrieve specific study details
- `GET /api/pico-comparisons/` - TTE vs RCT comparison data
- `GET /api/learning-resources/` - Educational resources
- `GET /api/statistics/` - Database statistics
- `GET /api/search/?q={query}` - Search studies

### **Example Usage**:
```python
import requests

# Get all studies
response = requests.get('https://ttedb.xeradb.com/api/studies/')
studies = response.json()

# Search for cardiovascular studies
response = requests.get('https://ttedb.xeradb.com/api/search/?q=cardiovascular')
results = response.json()
```

Full API documentation available at: [https://ttedb.xeradb.com/api/](https://ttedb.xeradb.com/api/)

## 📊 **Database Schema**

### **Core Models**:

- **TTEStudy**: Main study information, methodology, and metadata
- **PICOComparison**: TTE vs RCT comparison data and effect estimates
- **LearningResource**: Educational materials and methodology guides
- **DatabaseStatistic**: Pre-calculated analytics for performance optimization

### **Key Fields**:
- Study characteristics (disease, intervention, population)
- Methodological details (matching, analysis methods, DAG usage)
- Effect estimates (point estimates, confidence intervals, p-values)
- Transparency metrics (protocol registration, data sharing, funding)

## 🤝 **Contributing**

We welcome contributions from the research community! Here's how to get involved:

### **Study Submissions**
- Submit new TTE studies through our standardized form
- Provide complete PICO elements and effect estimates
- Include transparency and methodology details

### **Code Contributions**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### **Areas for Contribution**:
- Database curation and quality control
- Statistical analysis methods and visualizations
- Educational content development
- API enhancements and documentation
- User interface improvements

## 📋 **Research Protocol**

TTEdb follows a systematic research protocol for data collection and analysis. Key methodological aspects:

- **Systematic Search Strategy**: MEDLINE and Embase databases with standardized terms
- **Living Update Framework**: Automated PubMed monitoring for new studies
- **Quality Assessment**: Structured evaluation of study methodology and transparency
- **Bayesian Analysis**: Stratified meta-analysis by effect measure type
- **Bias Detection**: Comprehensive assessment of publication and selection bias

For detailed methodology, see [Protocol_TTE_MetaResearch.md](Protocol_TTE_MetaResearch.md).

## 📚 **Citation**

If you use TTEdb in your research, please cite:

```bibtex
@misc{ttedb2024,
  title={TTEdb: Target Trial Emulation Database},
  author={[Author Names]},
  year={2024},
  url={https://ttedb.xeradb.com},
  note={Accessed: [Date]}
}
```

## 🏆 **Acknowledgments**

- **Methodological Foundation**: Built on established TTE methodology frameworks
- **Open Science**: Committed to transparent and reproducible research practices
- **Community Contributions**: Grateful for submissions from the global research community
- **Technical Infrastructure**: Powered by Django, PostgreSQL, and modern web technologies

## 📞 **Support & Contact**

- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/choxos/TTEdb/issues)
- **Discussions**: Join methodological discussions in [GitHub Discussions](https://github.com/choxos/TTEdb/discussions)
- **Email**: Contact the development team at [contact information]
- **Documentation**: Comprehensive guides available in the `/docs` directory

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 **Roadmap**

### **Upcoming Features**:
- **Machine Learning Integration**: Automated study classification and quality assessment
- **Advanced Visualizations**: Interactive network analysis and causal diagrams
- **Collaborative Platform**: Multi-user study curation and peer review system
- **Mobile Application**: Native mobile access for field research
- **Integration APIs**: Connections with major research databases and registries

### **Research Initiatives**:
- **Methodological Guidelines**: Evidence-based recommendations for TTE studies
- **Quality Metrics**: Standardized assessment tools for TTE research
- **Educational Programs**: Training modules for researchers and students
- **International Collaboration**: Partnerships with research institutions worldwide

---

**TTEdb**: Advancing causal inference through systematic evidence synthesis and transparent research practices.

[![GitHub Stars](https://img.shields.io/github/stars/choxos/TTEdb?style=social)](https://github.com/choxos/TTEdb/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/choxos/TTEdb?style=social)](https://github.com/choxos/TTEdb/network/members)
[![Twitter Follow](https://img.shields.io/twitter/follow/TTEdb?style=social)](https://twitter.com/TTEdb)