import os
import json

# 1. SETUP PATHS
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, 'templates')
CONTENT_DIR = os.path.join(PROJECT_ROOT, 'content')
CONDITIONS_OUT_DIR = os.path.join(PROJECT_ROOT, 'conditions')
BLOG_OUT_DIR = os.path.join(PROJECT_ROOT, 'blog')

os.makedirs(CONDITIONS_OUT_DIR, exist_ok=True)
os.makedirs(BLOG_OUT_DIR, exist_ok=True)

# 2. LOAD DATA
with open(os.path.join(CONTENT_DIR, 'conditions.json'), 'r') as f:
    conditions_data = json.load(f)

with open(os.path.join(CONTENT_DIR, 'blog.json'), 'r') as f:
    blog_data = json.load(f)

# 3. SCHEMA.ORG GENERATORS
def get_base_physician_schema():
    schema = {
        "@context": "https://schema.org",
        "@type": "Physician",
        "name": "Dr. Ayesha Saeed",
        "image": "https://drayeshasaeed.com/assets/images/dr-ayesha.png",
        "medicalSpecialty": "PediatricOrthopedics",
        "qualification": [
            {
                "@type": "EducationalOccupationalCredential",
                "name": "FCPS Orthopedics",
                "credentialCategory": "Gold Medalist"
            },
            {
                "@type": "EducationalOccupationalCredential",
                "name": "Fellowship in Pediatric Orthopedics",
                "recognizedBy": {
                    "@type": "MedicalOrganization",
                    "name": "The Hospital for Sick Children (SickKids), Toronto, Canada"
                }
            }
        ],
        "knowsAbout": [
            "Clubfoot", "Developmental Dysplasia of the Hip", "Scoliosis", "Growth Plate Injuries", "Pediatric Fractures"
        ],
        "telephone": "+923000000000",
        "email": "inquire@drayeshasaeed.com",
        "url": "https://drayeshasaeed.com",
        "address": [
            {
                "@type": "PostalAddress",
                "streetAddress": "Medicare Cardiac & General Hospital, Shaheed-e-Millat Road",
                "addressLocality": "Karachi",
                "addressRegion": "Sindh",
                "addressCountry": "PK"
            },
            {
                "@type": "PostalAddress",
                "streetAddress": "Horizon Hospital, Johar Town",
                "addressLocality": "Lahore",
                "addressRegion": "Punjab",
                "addressCountry": "PK"
            }
        ]
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def get_faq_schema():
    faqs = [
        {"q": "What is the best age to treat clubfoot in a baby?", "a": "Clubfoot treatment using the Ponseti method should ideally begin within the first 1 to 2 weeks of life, when the baby's tendons and bones are highly flexible. However, the method is still highly effective for older babies."},
        {"q": "How do I know if my child's bow legs are normal or abnormal?", "a": "Bowing is normal (physiological) in infants and toddlers up to 18-24 months and usually straightens by age 2. If bowing affects only one leg, worsens after age 2, causes a limp, or is accompanied by short stature, it requires a clinical check-up to rule out Rickets or Blount's disease."},
        {"q": "What is a growth plate, and why is an injury there serious?", "a": "The growth plate is an area of active cartilage near the ends of a child's long bones where bone growth occurs. Because it is softer cartilage, it fractures easily. If a growth plate fracture is not properly aligned, the bone may stop growth or grow crookedly, leading to permanent leg or arm deformities."},
        {"q": "Does scoliosis always require major spinal surgery?", "a": "No. The vast majority of children with scoliosis have mild curves that require only regular observation. Moderate curves can be treated effectively using custom orthopedic braces to prevent the curve from worsening. Surgery (spinal fusion) is reserved for severe curves (usually over 45-50 degrees) that progress despite bracing."},
        {"q": "How is DDH (Hip Dysplasia) treated in newborn babies?", "a": "If diagnosed early (under 6 months), hip dysplasia is treated highly successfully with a Pavlik Harness. This is a soft fabric brace that keeps the baby's hips bent and spread open, allowing the joint to deepen naturally. It has a success rate of over 90% without surgery."}
    ]
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["a"]
                }
            } for item in faqs
        ]
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def get_breadcrumb_schema(crumbs):
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": item[0],
                "item": item[1]
            } for i, item in enumerate(crumbs)
        ]
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def get_condition_schema(condition_name, page_url):
    schema = {
        "@context": "https://schema.org",
        "@type": "MedicalWebPage",
        "url": page_url,
        "name": f"Guide to {condition_name}",
        "about": {
            "@type": "MedicalCondition",
            "name": condition_name,
            "associatedSpecialty": {
                "@type": "MedicalSpecialty",
                "name": "PediatricOrthopedics"
            }
        }
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def get_blog_schema(title, date, desc, page_url):
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "datePublished": date,
        "description": desc,
        "author": {
            "@type": "Person",
            "name": "Dr. Ayesha Saeed",
            "jobTitle": "Pediatric Orthopedic Surgeon"
        },
        "publisher": {
            "@type": "MedicalOrganization",
            "name": "Dr. Ayesha Saeed Pediatric Orthopedics",
            "logo": {
                "@type": "ImageObject",
                "url": "https://drayeshasaeed.com/assets/images/logo.png"
            }
        },
        "mainEntityOfPage": page_url
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

# 4. LOAD BASE TEMPLATE
with open(os.path.join(TEMPLATES_DIR, 'base.html'), 'r') as f:
    base_html = f.read()

# Helper to load specific page template
def get_page_template(name):
    with open(os.path.join(TEMPLATES_DIR, f"{name}.html"), 'r') as f:
        return f.read()

# 5. CORE COMPILER UTILITY
def compile_page(content_html, title, description, keywords, canonical, schema_html, relative_path, active_nav):
    # FIRST replace the CONTENT placeholder to embed child templates
    compiled = base_html.replace('{{ CONTENT }}', content_html)
    
    # THEN replace all other variables (which now covers placeholders inside child templates!)
    compiled = compiled.replace('{{ TITLE }}', title)
    compiled = compiled.replace('{{ DESCRIPTION }}', description)
    compiled = compiled.replace('{{ KEYWORDS }}', keywords)
    compiled = compiled.replace('{{ CANONICAL }}', canonical)
    compiled = compiled.replace('{{ SCHEMA }}', schema_html)
    compiled = compiled.replace('{{ RELATIVE_PATH }}', relative_path)
    
    # Set the active navigation link class
    if active_nav:
        compiled = compiled.replace(f'{{{{ {active_nav} }}}}', 'active')
        
    # Clear all other active flags
    nav_flags = ['ACTIVE_HOME', 'ACTIVE_ABOUT', 'ACTIVE_CONDITIONS', 'ACTIVE_TREATMENTS', 'ACTIVE_EDUCATION', 'ACTIVE_MEDIA', 'ACTIVE_FAQS', 'ACTIVE_CONTACT']
    for flag in nav_flags:
        compiled = compiled.replace(f'{{{{ {flag} }}}}', '')
        
    return compiled

# 6. COMPILE HOME (index.html)
print("Compiling index.html...")
index_content = get_page_template('index')
index_schema = get_base_physician_schema() + "\n" + get_faq_schema()

index_html = compile_page(
    content_html=index_content,
    title='Best Pediatric Orthopedic Surgeon in Karachi & Lahore | Dr. Ayesha Saeed',
    description='Dr. Ayesha Saeed is a Gold Medalist Pediatric Orthopedic Surgeon trained at SickKids Toronto, Canada. 10+ years experience in Clubfoot, DDH, Scoliosis.',
    keywords='Best Pediatric Orthopedic Surgeon in Karachi, Best Pediatric Orthopedic Surgeon in Lahore, Child Bone Specialist Pakistan, Dr. Ayesha Saeed',
    canonical='https://drayeshasaeed.com/index.html',
    schema_html=index_schema,
    relative_path='',
    active_nav='ACTIVE_HOME'
)

with open(os.path.join(PROJECT_ROOT, 'index.html'), 'w') as f:
    f.write(index_html)


# 7. COMPILE CONDITIONS OVERVIEW (conditions.html)
print("Compiling conditions.html...")

PEDIATRIC_THEME = {
    "clubfoot": {
        "color_class": "card-pastel-mint",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <path d="M7 16c-1 0-1.8.8-1.8 1.8c0 1.2 1.8 2.2 1.8 2.2s1.8-1 1.8-2.2c0-1-.8-1.8-1.8-1.8z" fill="currentColor" fill-opacity="0.2"/>
            <circle cx="7" cy="12" r="1" /><circle cx="10" cy="13" r="0.8" /><circle cx="4" cy="14" r="0.8" />
            <path d="M15 12c-1 0-1.8.8-1.8 1.8c0 1.2 1.8 2.2 1.8 2.2s1.8-1 1.8-2.2c0-1-.8-1.8-1.8-1.8z" fill="currentColor" fill-opacity="0.2"/>
            <circle cx="15" cy="8" r="1" /><circle cx="18" cy="9" r="0.8" /><circle cx="12" cy="10" r="0.8" />
        </svg>"""
    },
    "ddh": {
        "color_class": "card-pastel-sky",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <circle cx="12" cy="6" r="3" fill="currentColor" fill-opacity="0.1"/>
            <path d="M12 9v12M9 12h6M6 18c0-3 3-5 6-5s6 2 6 5" />
            <circle cx="6" cy="18" r="1.5" /><circle cx="18" cy="18" r="1.5" />
        </svg>"""
    },
    "bow-legs": {
        "color_class": "card-pastel-peach",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <circle cx="12" cy="4" r="2.5" fill="currentColor" fill-opacity="0.1"/>
            <path d="M12 6.5v6M9 9.5h6" />
            <path d="M9 12.5C6.5 15.5 6.5 19.5 8.5 22M15 12.5c2.5 3 2.5 7 .5 9.5" />
        </svg>"""
    },
    "knock-knees": {
        "color_class": "card-pastel-lavender",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <circle cx="12" cy="4" r="2.5" fill="currentColor" fill-opacity="0.1"/>
            <path d="M12 6.5v6M9 9.5h6" />
            <path d="M7.5 12.5C9.5 15 9.5 17 8 22M16.5 12.5C14.5 15 14.5 17 16 22" />
        </svg>"""
    },
    "flat-feet": {
        "color_class": "card-pastel-mint",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <path d="M3 12c0 2 2.5 3.5 5 3s4.5-2.5 8-2.5 5 1.5 5 3v1H3v-4.5z" fill="currentColor" fill-opacity="0.1"/>
            <path d="M6 15c2-2.5 4.5-2.5 7 0" stroke-dasharray="2 2" />
            <circle cx="5" cy="8" r="1" /><circle cx="8" cy="7" r="0.8" /><circle cx="11" cy="7.5" r="0.8" />
        </svg>"""
    },
    "rickets": {
        "color_class": "card-pastel-yellow",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <circle cx="12" cy="12" r="4" fill="currentColor" fill-opacity="0.15"/>
            <path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M5 19l1.5-1.5M17.5 6.5L19 5" />
            <path d="M10 10h4v4h-4z" />
        </svg>"""
    },
    "scoliosis": {
        "color_class": "card-pastel-lavender",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <path d="M12 2v2" />
            <path d="M12 4c-2 3-2 5 0 8s2 5 0 8" stroke-width="2.5" />
            <path d="M9 7h6M8 11h8M9 15h6M8 19h8" />
        </svg>"""
    },
    "growth-plate-injuries": {
        "color_class": "card-pastel-yellow",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <path d="M8 3h8v3c-1.5 1-1.5 3 0 4v8c-1.5 1-1.5 3 0 4v2H8v-2c1.5-1 1.5-3 0-4v-8c1.5-1 1.5-3 0-4V3z" fill="currentColor" fill-opacity="0.05"/>
            <line x1="8" y1="7" x2="16" y2="7" stroke="currentColor" stroke-width="3" />
            <line x1="8" y1="17" x2="16" y2="17" stroke="currentColor" stroke-width="3" />
        </svg>"""
    },
    "pediatric-fractures": {
        "color_class": "card-pastel-peach",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <path d="M7 6v14a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V6L12 3 7 6z" fill="currentColor" fill-opacity="0.1"/>
            <path d="M10 13h4M12 11v4" />
            <circle cx="10.5" cy="18" r="0.5" /><circle cx="13.5" cy="18" r="0.5" />
            <path d="M11 19.5c.5.5 1 .5 1.5 0" />
        </svg>"""
    },
    "sports-injuries": {
        "color_class": "card-pastel-sky",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <circle cx="12" cy="5" r="2.5" fill="currentColor" fill-opacity="0.1"/>
            <path d="M7 11.5l5-2 5 2M12 9.5v5l-3 4.5M12 14.5l3 3.5" />
            <circle cx="18" cy="18" r="2" />
        </svg>"""
    },
    "walking-problems": {
        "color_class": "card-pastel-mint",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <circle cx="10" cy="5" r="2.5" />
            <path d="M10 7.5c-1.5 2-1.5 5 0 8" />
            <path d="M7 12.5l3-2.5 3 2.5" />
            <path d="M8 21.5l2-5 3 5" />
            <path d="M17 11a2.5 2.5 0 0 1-2.5-2.5c0-1.5 2.5-4.5 2.5-4.5s2.5 3 2.5 4.5A2.5 2.5 0 0 1 17 11z" fill="currentColor" fill-opacity="0.2" />
        </svg>"""
    },
    "hip-disorders": {
        "color_class": "card-pastel-sky",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <circle cx="12" cy="7" r="3" fill="currentColor" fill-opacity="0.1"/>
            <path d="M8 12c2 1 6 1 8 0" />
            <path d="M6 19.5c1-2.5 3-4 6-4s5 1.5 6 4" />
        </svg>"""
    },
    "bone-deformities": {
        "color_class": "card-pastel-peach",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <path d="M8 4h8v2M8 20h8v-2" />
            <path d="M12 6v12" stroke-width="2.5" />
            <path d="M6 12h12" stroke-dasharray="2 2" />
        </svg>"""
    },
    "joint-pain": {
        "color_class": "card-pastel-lavender",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <circle cx="12" cy="12" r="7" fill="currentColor" fill-opacity="0.1"/>
            <path d="M12 8v8M8 12h8" />
            <circle cx="12" cy="12" r="2.5" />
        </svg>"""
    },
    "congenital-bone-conditions": {
        "color_class": "card-pastel-yellow",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <path d="M12 3a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5z" fill="currentColor" fill-opacity="0.15"/>
            <path d="M6 12h12M12 8v8M9 21l3-5 3 5" />
        </svg>"""
    },
    "posture-problems": {
        "color_class": "card-pastel-sky",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px;">
            <circle cx="12" cy="5" r="2.5" />
            <path d="M12 7.5v8.5H7.5M12 16l3 5" />
            <path d="M12 9.5h4.5" />
        </svg>"""
    }
}

conditions_grid = ""
for slug, cond in conditions_data.items():
    theme = PEDIATRIC_THEME.get(slug, {
        "color_class": "card-pastel-sky",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width: 32px; height: 32px;"><circle cx="12" cy="12" r="10"/><path d="M12 8v8M8 12h8"/></svg>"""
    })
    
    conditions_grid += f"""
    <div class="card condition-card reveal {theme['color_class']}">
        <div class="card-icon">
            {theme['svg']}
        </div>
        <h3>{cond['name']}</h3>
        <p>{cond['intro'][:110]}...</p>
        <a href="conditions/{slug}.html" class="card-link">
            Learn More <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width: 16px; height: 16px;"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
    </div>
    """

conditions_content = get_page_template('conditions').replace('{{ CONDITIONS_GRID }}', conditions_grid)
conditions_schema = get_breadcrumb_schema([("Home", "https://drayeshasaeed.com/index.html"), ("Conditions", "https://drayeshasaeed.com/conditions.html")])

cond_page_html = compile_page(
    content_html=conditions_content,
    title='Orthopedic Conditions Treated | Dr. Ayesha Saeed',
    description='Overview of bone, joint, muscle, and postural abnormalities treated by pediatric specialist Dr. Ayesha Saeed. Clubfoot, hip dysplasia, spine curvature, and fractures.',
    keywords='Child Bone Doctor, Pediatric Orthopedic Surgeon Pakistan, Flat Feet Treatment, Bow Legs Treatment',
    canonical='https://drayeshasaeed.com/conditions.html',
    schema_html=conditions_schema,
    relative_path='',
    active_nav='ACTIVE_CONDITIONS'
)

with open(os.path.join(PROJECT_ROOT, 'conditions.html'), 'w') as f:
    f.write(cond_page_html)


# 8. COMPILE TREATMENTS OVERVIEW (treatments.html)
print("Compiling treatments.html...")
treatments_content = get_page_template('treatments')
treatments_schema = get_breadcrumb_schema([("Home", "https://drayeshasaeed.com/index.html"), ("Treatments", "https://drayeshasaeed.com/treatments.html")])

treat_page_html = compile_page(
    content_html=treatments_content,
    title='Pediatric Orthopedic Treatments & Surgery | Dr. Ayesha Saeed',
    description='Advanced clinical treatments by Dr. Ayesha Saeed, including Ponseti clubfoot method, serial casting, pediatric trauma management, and growth-plate safe operations.',
    keywords='Ponseti Method Karachi, Pediatric Fracture Specialist, Growth Plate Injury Doctor',
    canonical='https://drayeshasaeed.com/treatments.html',
    schema_html=treatments_schema,
    relative_path='',
    active_nav='ACTIVE_TREATMENTS'
)

with open(os.path.join(PROJECT_ROOT, 'treatments.html'), 'w') as f:
    f.write(treat_page_html)


# 9. COMPILE PARENT EDUCATION OVERVIEW (education.html)
print("Compiling education.html...")

BLOG_ILLUSTRATIONS = {
    "Clubfoot & Deformities": {
        "color": "var(--color-mint-green)",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 48px; height: 48px;">
            <path d="M7 16c-0.8 0-1.5 0.6-1.5 1.5c0 1 1.5 1.8 1.5 1.8s1.5-0.8 1.5-1.8c0-0.9-0.7-1.5-1.5-1.5z" fill="currentColor" fill-opacity="0.2"/>
            <path d="M15 12c-0.8 0-1.5 0.6-1.5 1.5c0 1 1.5 1.8 1.5 1.8s1.5-0.8 1.5-1.8c0-0.9-0.7-1.5-1.5-1.5z" fill="currentColor" fill-opacity="0.2"/>
            <circle cx="7" cy="12" r="0.8" /><circle cx="9.5" cy="13" r="0.6" />
            <circle cx="15" cy="8" r="0.8" /><circle cx="17.5" cy="9" r="0.6" />
        </svg>"""
    },
    "Bone Development": {
        "color": "var(--color-warm-yellow)",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 48px; height: 48px;">
            <circle cx="12" cy="12" r="4" fill="currentColor" fill-opacity="0.15"/>
            <path d="M12 2v2M12 20v2M2 12h2M20 12h2" />
            <path d="M10 10h4v4h-4z" />
        </svg>"""
    },
    "Foot & Ankle": {
        "color": "var(--color-sky-blue)",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 48px; height: 48px;">
            <path d="M6 14V8a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2z" fill="currentColor" fill-opacity="0.1"/>
            <circle cx="12" cy="11" r="2.5" />
        </svg>"""
    },
    "Spine Health": {
        "color": "var(--color-lavender)",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 48px; height: 48px;">
            <path d="M12 2v2" />
            <path d="M12 4c-1.5 3-1.5 5 0 8s1.5 5 0 8" stroke-width="2.5" />
            <path d="M9 7h6M9 15h6" />
        </svg>"""
    },
    "Fractures & Trauma": {
        "color": "var(--color-peach)",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 48px; height: 48px;">
            <path d="M8 6v12a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V6L12 3z" fill="currentColor" fill-opacity="0.1"/>
            <path d="M10 13h4M12 11v4" />
        </svg>"""
    },
    "Posture & Habits": {
        "color": "var(--color-sky-blue)",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 48px; height: 48px;">
            <circle cx="12" cy="5" r="2.5" />
            <path d="M12 8v7M8 11h8M9 21h6" />
        </svg>"""
    },
    "Physical Health": {
        "color": "var(--color-mint-green)",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 48px; height: 48px;">
            <circle cx="12" cy="6" r="3" />
            <path d="M6 12l6-2 6 2M12 10v6l-3 4.5M12 16l3 4.5" />
        </svg>"""
    }
}

blog_grid = ""
for slug, article in blog_data.items():
    category = article['category']
    illustration = BLOG_ILLUSTRATIONS.get(category, {
        "color": "var(--color-primary-light)",
        "svg": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 48px; height: 48px;"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/></svg>"""
    })

    blog_grid += f"""
    <div class="card blog-card reveal card-tint-white" style="display: flex; flex-direction: column; height: 100%;">
        <div class="blog-img" style="height: 200px; overflow: hidden; position: relative;">
            <img src="{{{{ RELATIVE_PATH }}}}assets/images/blog/{slug}.jpg" alt="{article['title']}" style="width: 100%; height: 100%; object-fit: cover; display: block; transition: var(--transition-slow);">
        </div>
        <div class="blog-meta">
            <span class="badge" style="background-color: {illustration['color']}; color: var(--color-secondary); font-weight: 700; border-radius: var(--radius-sm); font-size: 0.78rem;">{article['category']}</span>
            <span style="font-size: 0.8rem; font-weight: 500; color: var(--color-text-light);"><i data-lucide="clock" style="width: 12px; height: 12px; display: inline; vertical-align: middle; margin-right: 2px;"></i> {article['read_time']}</span>
        </div>
        <div class="blog-content" style="display: flex; flex-direction: column; flex-grow: 1; justify-content: space-between;">
            <div>
                <h3><a href="blog/{slug}.html">{article['title']}</a></h3>
                <p>{article['intro'][:95]}...</p>
            </div>
            <a href="blog/{slug}.html" class="card-link" style="justify-content: flex-start; color: var(--color-primary); font-weight: 700; margin-top: var(--space-sm);">
                Read Article <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width: 16px; height: 16px;"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>
        </div>
    </div>
    """

education_content = get_page_template('education').replace('{{ BLOG_GRID }}', blog_grid)
education_schema = get_breadcrumb_schema([("Home", "https://drayeshasaeed.com/index.html"), ("Parent Education", "https://drayeshasaeed.com/education.html")])

edu_page_html = compile_page(
    content_html=education_content,
    title='Parent Education & Guides | Dr. Ayesha Saeed',
    description='Free educational articles and skeletal safety guides written by Pediatric Orthopedic Surgeon Dr. Ayesha Saeed. Swaddling, posture, flat feet, and sports safety.',
    keywords='Child bone guide, Rickets prevention, W-sitting dangers, Pediatric orthopedics blog',
    canonical='https://drayeshasaeed.com/education.html',
    schema_html=education_schema,
    relative_path='',
    active_nav='ACTIVE_EDUCATION'
)

with open(os.path.join(PROJECT_ROOT, 'education.html'), 'w') as f:
    f.write(edu_page_html)


# 10. COMPILE MEDIA (media.html)
print("Compiling media.html...")
media_content = get_page_template('media')
media_schema = get_breadcrumb_schema([("Home", "https://drayeshasaeed.com/index.html"), ("Media", "https://drayeshasaeed.com/media.html")])

media_page_html = compile_page(
    content_html=media_content,
    title='TV Interviews & Medical Media | Dr. Ayesha Saeed',
    description='Watch Dr. Ayesha Saeed\'s TV talk shows, public orthopedic presentations, and pediatric surgery clinical campaign archives.',
    keywords='Dr. Ayesha Saeed TV, Pediatric orthopedic media, Child bone awareness Pakistan',
    canonical='https://drayeshasaeed.com/media.html',
    schema_html=media_schema,
    relative_path='',
    active_nav='ACTIVE_MEDIA'
)

with open(os.path.join(PROJECT_ROOT, 'media.html'), 'w') as f:
    f.write(media_page_html)


# 11. COMPILE CONTACT (contact.html)
print("Compiling contact.html...")
contact_content = get_page_template('contact')
contact_schema = get_breadcrumb_schema([("Home", "https://drayeshasaeed.com/index.html"), ("Contact", "https://drayeshasaeed.com/contact.html")])

contact_page_html = compile_page(
    content_html=contact_content,
    title='Contact & Booking | Dr. Ayesha Saeed Pediatric Orthopedics',
    description='Book a consultation slot with Dr. Ayesha Saeed in Karachi at Medicare Hospital or in Lahore at Horizon Hospital. Coordinates, phone numbers, and location maps.',
    keywords='Pediatric Orthopedic Surgeon Karachi phone, Horizon Hospital Lahore timings, Book doctor appointment',
    canonical='https://drayeshasaeed.com/contact.html',
    schema_html=contact_schema,
    relative_path='',
    active_nav='ACTIVE_CONTACT'
)

with open(os.path.join(PROJECT_ROOT, 'contact.html'), 'w') as f:
    f.write(contact_page_html)


# 12. COMPILE 16 INDIVIDUAL CONDITION DETAIL PAGES (conditions/*.html)
print("Compiling 16 condition landing pages...")
condition_template = get_page_template('condition_detail')

for slug, cond in conditions_data.items():
    symptoms_list = "".join([f"<li>{sym}</li>\n" for sym in cond["symptoms"]])
    causes_list = "".join([f"<li>{caus}</li>\n" for caus in cond["causes"]])
    
    other_links = ""
    for c_slug, c_val in conditions_data.items():
        if c_slug != slug:
            other_links += f"""<a href="{c_slug}.html">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 14px; height: 14px;"><path d="m9 18 6-6-6-6"/></svg>
                {c_val['name'].split(' (')[0]}
            </a>\n"""
            
    related_blogs = ""
    for link in cond["internal_links"]:
        related_blogs += f"""<a href="{link['url']}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 14px; height: 14px;"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            {link['name']}
        </a>\n"""

    page_url = f"https://drayeshasaeed.com/conditions/{slug}.html"
    cond_schema = get_breadcrumb_schema([
        ("Home", "https://drayeshasaeed.com/index.html"),
        ("Conditions", "https://drayeshasaeed.com/conditions.html"),
        (cond["name"], page_url)
    ]) + "\n" + get_condition_schema(cond["name"], page_url)

    # Compile Template Content
    compiled_body = condition_template.replace('{{ NAME }}', cond['name'])
    compiled_body = compiled_body.replace('{{ INTRO }}', cond['intro'])
    compiled_body = compiled_body.replace('{{ SYMPTOMS_LIST }}', symptoms_list)
    compiled_body = compiled_body.replace('{{ CAUSES_LIST }}', causes_list)
    compiled_body = compiled_body.replace('{{ TREATMENT }}', cond['treatment'])
    compiled_body = compiled_body.replace('{{ OTHER_CONDITIONS_LINKS }}', other_links)
    compiled_body = compiled_body.replace('{{ RELATED_BLOG_LINKS }}', related_blogs)

    # Merge into base layout using compile_page
    page_html = compile_page(
        content_html=compiled_body,
        title=cond['seo_title'],
        description=cond['seo_description'],
        keywords=", ".join(cond['keywords']),
        canonical=page_url,
        schema_html=cond_schema,
        relative_path='../',
        active_nav='ACTIVE_CONDITIONS'
    )

    with open(os.path.join(CONDITIONS_OUT_DIR, f"{slug}.html"), 'w') as f:
        f.write(page_html)


# 13. COMPILE 14 INDIVIDUAL BLOG DETAIL PAGES (blog/*.html)
print("Compiling 14 blog article pages...")
blog_template = get_page_template('blog_detail')

for slug, article in blog_data.items():
    related_links = ""
    for r_slug in article["related_slugs"]:
        if r_slug in blog_data:
            related_links += f"""<a href="{r_slug}.html">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 14px; height: 14px;"><path d="m9 18 6-6-6-6"/></svg>
                {blog_data[r_slug]['title'][:40]}...
            </a>\n"""
            
    other_links = ""
    for b_slug, b_val in blog_data.items():
        if b_slug != slug and b_slug not in article["related_slugs"]:
            other_links += f"""<a href="{b_slug}.html">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 14px; height: 14px;"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/></svg>
                {b_val['title'][:40]}...
            </a>\n"""

    page_url = f"https://drayeshasaeed.com/blog/{slug}.html"
    art_schema = get_breadcrumb_schema([
        ("Home", "https://drayeshasaeed.com/index.html"),
        ("Parent Education", "https://drayeshasaeed.com/education.html"),
        (article["title"], page_url)
    ]) + "\n" + get_blog_schema(article["title"], article["date"], article["seo_description"], page_url)

    # Compile Template Content
    compiled_body = blog_template.replace('{{ TITLE }}', article['title'])
    compiled_body = compiled_body.replace('{{ SLUG }}', slug)
    compiled_body = compiled_body.replace('{{ CATEGORY }}', article['category'])
    compiled_body = compiled_body.replace('{{ READ_TIME }}', article['read_time'])
    compiled_body = compiled_body.replace('{{ DATE }}', article['date'])
    compiled_body = compiled_body.replace('{{ INTRO }}', article['intro'])
    compiled_body = compiled_body.replace('{{ CONTENT }}', article['content'])
    compiled_body = compiled_body.replace('{{ RELATED_ARTICLES_LINKS }}', related_links)
    compiled_body = compiled_body.replace('{{ OTHER_BLOG_LINKS }}', other_links)

    # Merge into base layout using compile_page
    page_html = compile_page(
        content_html=compiled_body,
        title=article['seo_title'],
        description=article['seo_description'],
        keywords=", ".join(article['keywords']),
        canonical=page_url,
        schema_html=art_schema,
        relative_path='../',
        active_nav='ACTIVE_EDUCATION'
    )

    with open(os.path.join(BLOG_OUT_DIR, f"{slug}.html"), 'w') as f:
        f.write(page_html)

# 14. GENERATE ROBOTS.TXT AND SITEMAP.XML FOR PERFECT SEO
print("Generating sitemap.xml and robots.txt...")

sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://drayeshasaeed.com/index.html</loc><priority>1.0</priority></url>
  <url><loc>https://drayeshasaeed.com/conditions.html</loc><priority>0.8</priority></url>
  <url><loc>https://drayeshasaeed.com/treatments.html</loc><priority>0.8</priority></url>
  <url><loc>https://drayeshasaeed.com/education.html</loc><priority>0.8</priority></url>
  <url><loc>https://drayeshasaeed.com/media.html</loc><priority>0.7</priority></url>
  <url><loc>https://drayeshasaeed.com/contact.html</loc><priority>0.8</priority></url>
"""
for slug in conditions_data.keys():
    sitemap_xml += f"  <url><loc>https://drayeshasaeed.com/conditions/{slug}.html</loc><priority>0.7</priority></url>\n"
for slug in blog_data.keys():
    sitemap_xml += f"  <url><loc>https://drayeshasaeed.com/blog/{slug}.html</loc><priority>0.7</priority></url>\n"
sitemap_xml += "</urlset>"

with open(os.path.join(PROJECT_ROOT, 'sitemap.xml'), 'w') as f:
    f.write(sitemap_xml)

robots_txt = """User-agent: *
Allow: /

Sitemap: https://drayeshasaeed.com/sitemap.xml
"""

with open(os.path.join(PROJECT_ROOT, 'robots.txt'), 'w') as f:
    f.write(robots_txt)

print("Build complete! All 36 static pages generated successfully.")
