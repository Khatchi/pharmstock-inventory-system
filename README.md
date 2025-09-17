# PharmStock - Pharmacy Inventory Management System

A comprehensive web application for pharmacies to track medication inventory, manage stock levels, monitor expiration dates, and generate automated alerts for reordering.

## 🎯 Project Overview

**Target Users:** Pharmacy staff, inventory managers, and pharmacy owners  
**Value Proposition:** Reduces medication waste, prevents stockouts, ensures regulatory compliance, and streamlines inventory operations.

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 4.2+ with Django REST Framework
- **Database:** PostgreSQL 15+
- **Authentication:** Django Simple JWT
- **Configuration:** Django-environ
- **Additional:** Django CORS Headers, Django Filter

### Frontend
- **Framework:** React 18+ with TypeScript
- **State Management:** React Query + Context API
- **UI Library:** Material-UI or Tailwind CSS
- **HTTP Client:** Axios
- **Routing:** React Router

### Development Tools
- **IDE:** Tarae IDE with integrated AI agents
- **AI Models:** Gemini 2.5 Flash, Claude Sonnet 3.4/3.7/4, GPT-4.1
- **Version Control:** Git with GitHub
- **API Documentation:** Django REST Framework browsable API + OpenAPI schema

## 🧠 AI Integration Strategy

### Code Generation
- **Django Models:** Generate inventory, medication, supplier, and transaction models with proper relationships
- **API Endpoints:** Scaffold CRUD operations for all entities with proper serializers and viewsets
- **React Components:** Create reusable UI components for inventory tables, forms, and dashboards
- **Business Logic:** Generate inventory calculation functions, alert systems, and reporting utilities

### Testing Support
- **Backend Testing:**
  - Unit tests for models, serializers, and views using Django TestCase
  - API integration tests using DRF APITestCase
  - Authentication and permission tests
- **Frontend Testing:**
  - Component tests using React Testing Library
  - Integration tests for API interactions
  - Mock data generation for testing scenarios

### Schema-Aware Generation
- **OpenAPI Integration:** Use Django REST Framework's schema generation to feed API specs to AI
- **Database Schema Context:** Provide model definitions for relationship-aware code generation
- **Type-Safe Frontend:** Generate TypeScript interfaces from API responses
- **API Client Generation:** Create typed API service functions based on OpenAPI spec

### Documentation
- **Code Documentation:**
  - Auto-generated docstrings for Python functions and classes
  - JSDoc comments for React components and utility functions
  - Inline comments explaining complex business logic
- **Project Documentation:**
  - API documentation using DRF browsable API
  - Component documentation with usage examples
  - Setup and deployment guides

### Context-Aware Techniques
- **File Tree Context:** Provide project structure for consistent naming and organization
- **Schema Context:** Include database models and API schemas for accurate code generation
- **Diff Analysis:** Use git diffs for targeted code improvements and bug fixes
- **Requirements Context:** Reference user stories and acceptance criteria for feature development

## 🤖 AI Tools & Workflow

### In-Editor Integration (Tarae IDE)
- Real-time code suggestions and completions
- Automated code review and optimization suggestions
- Context-aware refactoring recommendations

### PR Review Process
- AI-generated commit messages following conventional commits
- Automated code quality checks and suggestions
- Documentation updates based on code changes

## 📝 Sample Prompting Strategy

### Code Generation Example
```
Generate a Django model for pharmaceutical inventory with the following requirements:
- Medication details (name, generic_name, dosage, form)
- Stock tracking (current_stock, minimum_threshold, maximum_capacity)
- Batch information (batch_number, expiry_date, supplier)
- Audit fields (created_at, updated_at, created_by)
Include proper field validation, model methods for stock calculations, and Meta class with appropriate indexing.
```

### Testing Example
```
Create comprehensive test suite for the inventory API endpoint including:
- CRUD operations testing with valid/invalid data
- Authentication and permission testing
- Edge cases: negative stock, expired medications, duplicate batch numbers
- Performance testing for bulk operations
Use Django APITestCase with proper fixtures and mock data.
```

## 🚀 Development Roadmap

### Phase 1: Core Backend (Day1)
- [ ] Database models and migrations
- [ ] Authentication system setup
- [ ] Basic CRUD API endpoints
- [ ] Django admin interface configuration

### Phase 2: Business Logic (Day2)
- [ ] Inventory calculation algorithms
- [ ] Alert system for low stock/expiry warnings
- [ ] Reporting and analytics endpoints
- [ ] Data validation and business rules

### Phase 3: Frontend Foundation (Day3)
- [ ] React app setup with TypeScript
- [ ] Authentication flow implementation
- [ ] Basic inventory management interface
- [ ] API integration and error handling

### Phase 4: Advanced Features (Day3)
- [ ] Dashboard with charts and analytics
- [ ] Advanced filtering and search functionality
- [ ] Batch operations and bulk updates
- [ ] Real-time notifications and alerts

### Phase 5: Testing & Deployment (Day4)
- [ ] Comprehensive testing suite
- [ ] Production deployment setup
- [ ] Performance optimization
- [ ] Security hardening and compliance

## 📋 Core Features

### Inventory Management
- Track medication stock levels in real-time
- Monitor expiration dates and batch information
- Automated low-stock and expiry alerts
- Supplier management and purchase order tracking

### Reporting & Analytics
- Stock movement reports
- Expiry and waste analysis
- Sales and usage patterns
- Regulatory compliance reporting

### User Management
- Role-based access control
- Audit trails for all transactions
- Multi-pharmacy support
- Staff activity monitoring

## 🏗️ Project Structure

```
pharmstock-inventory-system/
├── backend/
│   ├── pharmstock/           # Django project
│   ├── apps/                 # Django apps
│   │   ├── inventory/        # Inventory management
│   │   ├── medications/      # Medication catalog
│   │   ├── suppliers/        # Supplier management
│   │   └── users/           # User management
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   └── utils/           # Utility functions
│   ├── package.json
│   └── tsconfig.json
├── docs/                    # Documentation
├── tests/                   # Test files
└── README.md
```

## 🔧 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 15+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/Khatchi/pharmstock-inventory-system.git
cd pharmstock-inventory-system

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# Frontend setup
cd ../frontend
npm install
npm start
```

## 🧪 Testing Strategy

### Backend Testing
- Unit tests for all models and business logic
- API endpoint testing with comprehensive coverage
- Integration tests for complex workflows
- Performance testing for bulk operations

### Frontend Testing
- Component unit tests with React Testing Library
- Integration tests for user workflows
- End-to-end testing for critical paths
- Accessibility testing compliance

## 📚 Documentation

- **API Documentation:** Available at `/api/docs/` when running the development server
- **Component Library:** Storybook documentation for React components
- **Developer Guide:** Detailed setup and contribution guidelines
- **User Manual:** End-user documentation and tutorials

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Developer:** Solomon Ngwu
- **AI Assistants:** Gemini 2.5 Flash, Claude Sonnet 3.4/3.7/4, GPT-4.1, Trae IDE

---

**Built with ❤️ using Django, React, and AI-assisted development**