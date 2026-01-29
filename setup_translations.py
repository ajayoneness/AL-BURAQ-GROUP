import os
import struct

def output_mofile(msg_dict, output_file):
    messages = []
    for msgid, msgstr in msg_dict.items():
        # Include header (empty msgid)
        messages.append((msgid.encode('utf-8'), msgstr.encode('utf-8')))
    messages.sort()
    count = len(messages)
    header_size = 7 * 4
    ids_offset = header_size
    strs_offset = ids_offset + (8 * count)
    
    keys_blob = bytearray()
    key_descriptors = []
    current_key_off = strs_offset + (8 * count)
    
    for mid, mstr in messages:
        l = len(mid)
        key_descriptors.append((l, current_key_off))
        keys_blob.extend(mid)
        keys_blob.append(0)
        current_key_off += l + 1
        
    vals_blob = bytearray()
    val_descriptors = []
    current_val_off = current_key_off
    
    for mid, mstr in messages:
        l = len(mstr)
        val_descriptors.append((l, current_val_off))
        vals_blob.extend(mstr)
        vals_blob.append(0)
        current_val_off += l + 1
        
    with open(output_file, 'wb') as f:
        f.write(struct.pack('<I', 0x950412de))
        f.write(struct.pack('<I', 0))
        f.write(struct.pack('<I', count))
        f.write(struct.pack('<I', ids_offset))
        f.write(struct.pack('<I', strs_offset))
        f.write(struct.pack('<I', 0))
        f.write(struct.pack('<I', 0))
        for l, o in key_descriptors: f.write(struct.pack('<II', l, o))
        for l, o in val_descriptors: f.write(struct.pack('<II', l, o))
        f.write(keys_blob)
        f.write(vals_blob)

# ARABIC
translations_ar = {
    "": "Content-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n",
    "Services": "خدماتنا",
    "Our Services": "خدماتنا",
    "Our": "خدماتنا", 
    "Comprehensive trade and logistics solutions for your business": "حلول تجارية ولوجستية شاملة لأعمالك",
    "Comprehensive trade and logistics solutions tailored to your needs": "حلول تجارية ولوجستية شاملة مصممة خصيصاً لاحتياجاتك",
    
    "Air Shipping": "الشحن الجوي",
    "Fast and reliable air freight services for time-sensitive shipments. Ideal for urgent orders and high-value goods that need quick delivery worldwide.": "خدمات الشحن الجوي السريعة والموثوقة للشحنات الحساسة للوقت. مثالية للطلبات العاجلة والبضائع ذات القيمة العالية التي تحتاج إلى تسليم سريع في جميع أنحاء العالم.",
    "Fast and reliable air freight services for time-sensitive shipments worldwide.": "خدمات شحن جوي سريعة وموثوقة للشحنات الحساسة للوقت في جميع أنحاء العالم.",
    "Delivery in 3-7 days": "التسليم في 3-7 أيام",
    "Door-to-door service": "خدمة من الباب إلى الباب",
    "Real-time tracking": "تتبع في الوقت الحقيقي",
    
    "Sea Shipping": "الشحن البحري",
    "Cost-effective ocean freight for bulk shipments. Perfect for large orders where time is flexible but cost efficiency is paramount.": "شحن بحري فعال من حيث التكلفة للشحنات الضخمة. مثالي للطلبات الكبيرة حيث يكون الوقت مرنًا ولكن الكفاءة من حيث التكلفة هي الأهم.",
    "Cost-effective sea freight solutions for bulk and large shipments.": "حلول شحن بحري فعالة من حيث التكلفة للشحنات الضخمة والكبيرة.",
    "FCL & LCL options": "خيارات FCL و LCL",
    "Major ports worldwide": "الموانئ الرئيسية في جميع أنحاء العالم",
    "Competitive rates": "أسعار تنافسية",
    
    "Land Shipping": "الشحن البري",
    "Rail and road freight connecting China to Central Asia, Middle East, and Europe via the Belt and Road routes.": "الشحن عبر السكك الحديدية والطرق البرية الذي يربط الصين بآسيا الوسطى والشرق الأوسط وأوروبا عبر طرق الحزام والطريق.",
    "Efficient rail and road transport connecting China to Central Asia and Europe.": "نقل فعال بالسكك الحديدية والطرق يربط الصين بآسيا الوسطى وأوروبا.",
    "China-Europe Express": "قطار الصين-أوروبا السريع",
    "Faster than sea freight": "أسرع من الشحن البحري",
    "Regular departures": "رحلات منتظمة",
    
    "Sourcing & Purchasing": "التوريد والشراء",
    "Sourcing": "التوريد",
    "Expert product sourcing from verified Chinese manufacturers. We find the best suppliers and negotiate the best prices for you.": "توريد منتجات خبير من مصنعين صينيين تم التحقق منهم. نجد أفضل الموردين ونتفاوض على أفضل الأسعار لك.",
    "Expert product sourcing from verified Chinese manufacturers and suppliers.": "توريد منتجات خبير من مصنعين وموردين صينيين تم التحقق منهم.",
    "Factory verification": "التحقق من المصنع",
    "Price negotiation": "التفاوض على السعر",
    "Sample management": "إدارة العينات",
    
    "Quality Control": "مراقبة الجودة",
    "Rigorous quality inspection at every stage. Our QC team ensures     products meet your specifications before shipping.": "فحص دقيق للجودة في كل مرحلة. يضمن فريق مراقبة الجودة لدينا أن المنتجات تلبي مواصفاتك قبل الشحن.",
    "Rigorous quality inspection at every stage. Our QC team ensures products meet your specifications before shipping.": "فحص دقيق للجودة في كل مرحلة. يضمن فريق مراقبة الجودة لدينا أن المنتجات تلبي مواصفاتك قبل الشحن.",
    "Rigorous quality inspection to ensure products meet your standards.": "فحص صارم للجودة لضمان تلبية المنتجات لمعاييرك.",
    "Pre-shipment inspection": "فحص ما قبل الشحن",
    "Detailed reports": "تقارير مفصلة",
    "Photo documentation": "توثيق بالصور",
    
    "Assembly & Packing": "التجميع والتغليف",
    "Packing & Assembly": "التغليف والتجميع",
    "Professional packaging and assembly services. We consolidate products from multiple suppliers and pack according to your requirements.": "خدمات تغليف وتجميع احترافية. نقوم بدمج المنتجات من موردين متعددين وتغليفها وفقًا لمتطلباتك.",
    "Professional packaging and assembly services for your products.": "خدمات تغليف وتجميع احترافية لمنتجاتك.",
    "Custom packaging": "تغليف مخصص",
    "Labeling & branding": "وضع العلامات والعلامات التجارية",
    "Consolidation": "تجميع الشحنات",
    
    "Documentation & Customs": "التوثيق والجمارك",
    "Documentation": "التوثيق",
    "Complete customs clearance and documentation handling. We   navigate complex regulations so you don't have to.": "تخليص جمركي كامل ومعالجة الوثائق. نتنقل عبر اللوائح المعقدة حتى لا تضطر لذلك.",
    "Complete customs clearance and documentation handling. We navigate complex regulations so you don't have to.": "تخليص جمركي كامل ومعالجة الوثائق. نتنقل عبر اللوائح المعقدة حتى لا تضطر لذلك.",
    "Complete customs clearance and documentation handling.": "تخليص جمركي كامل ومعالجة الوثائق.",
    "Export documentation": "وثائق التصدير",
    "Customs clearance": "التخليص الجمركي",
    "Compliance consulting": "استشارات الامتثال",
    
    "Mechanism of Action": "آلية العمل",
    "A streamlined process from order to delivery. We handle every step of your import journey with precision and care.": "عملية مبسطة من الطلب إلى التسليم. نتعامل مع كل خطوة في رحلة الاستيراد الخاصة بك بدقة وعناية.",
    "End-to-end management": "إدارة شاملة",
    "Regular updates": "تحديثات منتظمة",
    "Dedicated support": "دعم مخصص",
    "24/7 Support": "دعم على مدار الساعة",
    "Dedicated support team available round the clock for assistance.": "فريق دعم مخصص متاح على مدار الساعة للمساعدة.",
    
    "Success Stories": "قصص النجاح",
    "Join hundreds of satisfied clients who have grown their businesses with AL BURAQ GROUP. Our track record speaks for itself.": "انضم إلى مئات العملاء الراضين الذين نموا أعمالهم مع مجموعة البراق. سجلنا يتحدث عن نفسه.",
    "View Case Studies": "عرض دراسات الحالة",
    "Success": "قصص",
    "Stories": "النجاح",
    
    "Need a Custom Solution?": "هل تحتاج إلى حل مخصص؟",
    "Contact us to discuss your specific requirements and get a tailored quote.": "اتصل بنا لمناقشة متطلباتك الخاصة والحصول على عرض أسعار مخصص.",
    "Get a Quote": "احصل على عرض أسعار",
    "Chat on WhatsApp": "دردشة عبر واتساب",
    "Ready to Start Your Import Business?": "هل أنت مستعد لبدء أعمال الاستيراد الخاصة بك؟",
    "Join thousands of satisfied clients who trust AL BURAQ GROUP for their sourcing and logistics needs.": "انضم إلى آلاف العملاء الراضين الذين يثقون في مجموعة البراق لاحتياجاتهم من التوريد والخدمات اللوجستية.",
    "Create Account": "إنشاء حساب",
    "Contact Us": "اتصل بنا",
    
    "Home": "الرئيسية",
    "About Us": "من نحن",
    "Store": "المتجر",
    "Tracking": "تتبع الشحنة",
    "Track Shipment": "تتبع الشحنة",
    "Track Now": "تتبع الآن",
    "Enter tracking number...": "أدخل رقم التتبع...",
    "Track Your Shipment": "تتبع شحنتك",
    "FAQ": "الأسئلة الشائعة",
    "Contact": "اتصل بنا",
    "Login": "تسجيل الدخول",
    "Logout": "تسجيل الخروج",
    "Profile": "الملف الشخصي",
    "Browse Store": "تصفح المتجر",
    "AL BURAQ GROUP - International Trade & Logistics": "مجموعة البراق - التجارة الدولية والخدمات اللوجستية",
    "Your Gateway to": "بوابتك إلى",
    "Global Trade": "التجارة العالمية",
    "Specialized in international trade, sourcing, and logistics from China to the world. Quality products, reliable shipping, exceptional service.": "متخصصون في التجارة الدولية والتوريد والخدمات اللوجستية من الصين إلى العالم. منتجات عالية الجودة، شحن موثوق، وخدمة استثنائية.",
    "Product": "تصنيفات",
    "Categories": "المنتجات",
    "Browse Our": "تصفح",
    "Products": "منتجاتنا",
    "Browse All Products": "تصفح جميع المنتجات",
    "Edit Profile": "تعديل الملف الشخصي",
    "First Name": "الاسم الأول",
    "Last Name": "اسم العائلة",
    "Email": "البريد الإلكتروني",
    "Phone": "الهاتف",
    "Company": "الشركة",
    "Country": "الدولة",
    "Address": "العنوان",
    "Save Changes": "حفظ التغييرات",
    "Cancel": "إلغاء",
    "Welcome,": "مرحباً،",
    "Manage your account and orders": "إدارة حسابك وطلباتك",
    "Frequently Asked": "الأسئلة",
    "Questions": "الشائعة",
    
    "Years Experience": "سنوات من الخبرة",
    "Countries Served": "الدول المخدومة",
    "Happy Clients": "عملاء سعداء",
    "View All Services": "عرض جميع الخدمات",
    "Explore our wide range of wholesale products from China": "استكشف مجموعتنا الواسعة من المنتجات بالجملة من الصين",
    "products": "منتجات",
    "Categories coming soon...": "التصنيفات قريبا...",
    "Why Choose": "لماذا تختار",
    "With over 10 years of experience in international trade, we have built a reputation for reliability, quality, and exceptional customer service.": "مع أكثر من 10 سنوات من الخبرة في التجارة الدولية، بنينا سمعة طيبة من حيث الموثوقية والجودة وخدمة العملاء الاستثنائية.",
    "Quality Guaranteed": "جودة مضمونة",
    "Rigorous quality control on all products": "مراقبة جودة صارمة على جميع المنتجات",
    "Competitive Prices": "أسعار تنافسية",
    "Direct factory prices without middlemen": "أسعار المصنع مباشرة بدون وسطاء",
    "Global Shipping": "شحن عالمي",
    "Delivery to 50+ countries worldwide": "التسليم لأكثر من 50 دولة حول العالم",
    "Dedicated Support": "دعم مخصص",
    "Multilingual team available 24/7": "فريق متعدد اللغات متاح 24/7",
    "Need help? Contact us directly:": "تحتاج مساعدة؟ اتصل بنا مباشرة:",
    "Offices": "مكاتبنا",
    "Visit our offices in China for personalized service": "تفضل بزيارة مكاتبنا في الصين للحصول على خدمة مخصصة",
}

# FRENCH
translations_fr = {
    "": "Content-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n",
    "Services": "Services",
    "Our Services": "Nos Services",
    "Our": "Nos",
    "Comprehensive trade and logistics solutions for your business": "Solutions complètes de commerce et de logistique pour votre entreprise",
    "Comprehensive trade and logistics solutions tailored to your needs": "Solutions complètes de commerce et de logistique adaptées à vos besoins",
    
    "Air Shipping": "Transport Aérien",
    "Fast and reliable air freight services for time-sensitive shipments. Ideal for urgent orders and high-value goods that need quick delivery worldwide.": "Services de fret aérien rapides et fiables pour les envois urgents. Idéal pour les commandes urgentes et les marchandises de grande valeur nécessitant une livraison rapide dans le monde entier.",
    "Fast and reliable air freight services for time-sensitive shipments worldwide.": "Services de fret aérien rapides et fiables pour les envois urgents dans le monde entier.",
    "Delivery in 3-7 days": "Livraison en 3-7 jours",
    "Door-to-door service": "Service porte-à-porte",
    "Real-time tracking": "Suivi en temps réel",
    
    "Sea Shipping": "Transport Maritime",
    "Cost-effective ocean freight for bulk shipments. Perfect for large orders where time is flexible but cost efficiency is paramount.": "Fret maritime économique pour les expéditions en vrac. Parfait pour les grosses commandes où le temps est flexible mais l'efficacité des coûts est primordiale.",
    "Cost-effective sea freight solutions for bulk and large shipments.": "Solutions de fret maritime économiques pour les expéditions en vrac et volumineuses.",
    "FCL & LCL options": "Options FCL & LCL",
    "Major ports worldwide": "Principaux ports du monde",
    "Competitive rates": "Tarifs compétitifs",
    
    "Land Shipping": "Transport Terrestre",
    "Rail and road freight connecting China to Central Asia, Middle East, and Europe via the Belt and Road routes.": "Fret ferroviaire et routier reliant la Chine à l'Asie centrale, au Moyen-Orient et à l'Europe via les routes de la soie.",
    "Efficient rail and road transport connecting China to Central Asia and Europe.": "Transport ferroviaire et routier efficace reliant la Chine à l'Asie centrale et à l'Europe.",
    "China-Europe Express": "China-Europe Express",
    "Faster than sea freight": "Plus rapide que le fret maritime",
    "Regular departures": "Départs réguliers",
    
    "Sourcing & Purchasing": "Sourcing & Achats",
    "Sourcing": "Sourcing",
    "Expert product sourcing from verified Chinese manufacturers. We find the best suppliers and negotiate the best prices for you.": "Sourcing expert de produits auprès de fabricants chinois vérifiés. Nous trouvons les meilleurs fournisseurs et négocions les meilleurs prix pour vous.",
    "Expert product sourcing from verified Chinese manufacturers and suppliers.": "Sourcing expert de produits auprès de fabricants et fournisseurs chinois vérifiés.",
    "Factory verification": "Vérification d'usine",
    "Price negotiation": "Négociation de prix",
    "Sample management": "Gestion des échantillons",
    
    "Quality Control": "Contrôle Qualité",
    "Rigorous quality inspection at every stage. Our QC team ensures     products meet your specifications before shipping.": "Inspection rigoureuse de la qualité à chaque étape. Notre équipe QC s'assure que les produits répondent à vos spécifications avant l'expédition.",
    "Rigorous quality inspection at every stage. Our QC team ensures products meet your specifications before shipping.": "Inspection rigoureuse de la qualité à chaque étape. Notre équipe QC s'assure que les produits répondent à vos spécifications avant l'expédition.",
    "Rigorous quality inspection to ensure products meet your standards.": "Inspection rigoureuse de la qualité pour garantir que les produits répondent à vos normes.",
    "Pre-shipment inspection": "Inspection avant expédition",
    "Detailed reports": "Rapports détaillés",
    "Photo documentation": "Documentation photo",
    
    "Assembly & Packing": "Assemblage & Emballage",
    "Packing & Assembly": "Emballage & Assemblage",
    "Professional packaging and assembly services. We consolidate products from multiple suppliers and pack according to your requirements.": "Services professionnels d'emballage et d'assemblage. Nous regroupons les produits de plusieurs fournisseurs et les emballons selon vos besoins.",
    "Professional packaging and assembly services for your products.": "Services professionnels d'emballage et d'assemblage pour vos produits.",
    "Custom packaging": "Emballage personnalisé",
    "Labeling & branding": "Étiquetage et image de marque",
    "Consolidation": "Consolidation",
    
    "Documentation & Customs": "Documentation & Douanes",
    "Documentation": "Documentation",
    "Complete customs clearance and documentation handling. We   navigate complex regulations so you don't have to.": "Dédouanement complet et gestion de la documentation. Nous naviguons dans les réglementations complexes pour vous.",
    "Complete customs clearance and documentation handling. We navigate complex regulations so you don't have to.": "Dédouanement complet et gestion de la documentation. Nous naviguons dans les réglementations complexes pour vous.",
    "Complete customs clearance and documentation handling.": "Dédouanement complet et gestion de la documentation.",
    "Export documentation": "Documentation d'exportation",
    "Customs clearance": "Dédouanement",
    "Compliance consulting": "Conseil en conformité",
    
    "Mechanism of Action": "Mécanisme d'Action",
    "A streamlined process from order to delivery. We handle every step of your import journey with precision and care.": "Un processus rationalisé de la commande à la livraison. Nous gérons chaque étape de votre parcours d'importation avec précision et soin.",
    "End-to-end management": "Gestion de bout en bout",
    "Regular updates": "Mises à jour régulières",
    "Dedicated support": "Support dédié",
    "24/7 Support": "Support 24/7",
    "Dedicated support team available round the clock for assistance.": "Équipe de support dédiée disponible 24h/24 pour assistance.",
    
    "Success Stories": "Histoires à succès",
    "Join hundreds of satisfied clients who have grown their businesses with AL BURAQ GROUP. Our track record speaks for itself.": "Rejoignez des centaines de clients satisfaits qui ont développé leurs activités avec AL BURAQ GROUP. Nos résultats parlent d'eux-mêmes.",
    "View Case Studies": "Voir les études de cas",
    "Success": "Succès",
    "Stories": "Histoires",
    
    "Need a Custom Solution?": "Besoin d'une solution personnalisée ?",
    "Contact us to discuss your specific requirements and get a tailored quote.": "Contactez-nous pour discuter de vos besoins spécifiques et obtenir un devis sur mesure.",
    "Get a Quote": "Obtenir un devis",
    "Chat on WhatsApp": "Discuter sur WhatsApp",
    "Ready to Start Your Import Business?": "Prêt à démarrer votre entreprise d'importation ?",
    "Join thousands of satisfied clients who trust AL BURAQ GROUP for their sourcing and logistics needs.": "Rejoignez des milliers de clients satisfaits qui font confiance à AL BURAQ GROUP pour leurs besoins d'approvisionnement et de logistique.",
    "Create Account": "Créer un compte",
    "Contact Us": "Contactez-nous",
    
    "Home": "Accueil",
    "About Us": "À propos",
    "Store": "Boutique",
    "Tracking": "Suivi",
    "Track Shipment": "Suivre l'envoi",
    "Track Now": "Suivre maintenant",
    "Enter tracking number...": "Entrez le numéro de suivi...",
    "Track Your Shipment": "Suivez votre envoi",
    "FAQ": "FAQ",
    "Contact": "Contact",
    "Login": "Connexion",
    "Logout": "Déconnexion",
    "Profile": "Profil",
    "Browse Store": "Parcourir la boutique",
    "AL BURAQ GROUP - International Trade & Logistics": "AL BURAQ GROUP - Commerce International & Logistique",
    "Your Gateway to": "Votre passerelle vers",
    "Global Trade": "Le Commerce Mondial",
    "Specialized in international trade, sourcing, and logistics from China to the world. Quality products, reliable shipping, exceptional service.": "Spécialisé dans le commerce international, le sourcing et la logistique de la Chine vers le monde. Produits de qualité, expédition fiable, service exceptionnel.",
    "Product": "Catégories",
    "Categories": "de Produits",
    "Browse Our": "Parcourir",
    "Products": "Nos Produits",
    "Browse All Products": "Voir tous les produits",
    "Edit Profile": "Modifier le profil",
    "First Name": "Prénom",
    "Last Name": "Nom",
    "Email": "Email",
    "Phone": "Téléphone",
    "Company": "Entreprise",
    "Country": "Pays",
    "Address": "Adresse",
    "Save Changes": "Enregistrer",
    "Cancel": "Annuler",
    "Welcome,": "Bienvenue,",
    "Manage your account and orders": "Gérer votre compte et vos commandes",
    "Frequently Asked": "Questions",
    "Questions": "Fréquentes",
    
    "Years Experience": "Années d'expérience",
    "Countries Served": "Pays desservis",
    "Happy Clients": "Clients satisfaits",
    "View All Services": "Voir tous les services",
    "Explore our wide range of wholesale products from China": "Explorez notre large gamme de produits de gros en provenance de Chine",
    "products": "produits",
    "Categories coming soon...": "Catégories bientôt disponibles...",
    "Why Choose": "Pourquoi choisir",
    "With over 10 years of experience in international trade, we have built a reputation for reliability, quality, and exceptional customer service.": "Avec plus de 10 ans d'expérience dans le commerce international, nous avons bâti une réputation de fiabilité, de qualité et de service client exceptionnel.",
    "Quality Guaranteed": "Qualité garantie",
    "Rigorous quality control on all products": "Contrôle qualité rigoureux sur tous les produits",
    "Competitive Prices": "Prix compétitifs",
    "Direct factory prices without middlemen": "Prix d'usine directs sans intermédiaires",
    "Global Shipping": "Expédition mondiale",
    "Delivery to 50+ countries worldwide": "Livraison dans plus de 50 pays",
    "Dedicated Support": "Support dédié",
    "Multilingual team available 24/7": "Équipe multilingue disponible 24/7",
    "Need help? Contact us directly:": "Besoin d'aide ? Contactez-nous directement :",
    "Offices": "Bureaux",
    "Visit our offices in China for personalized service": "Visitez nos bureaux en Chine pour un service personnalisé",
}

if __name__ == "__main__":
    # Arabic
    locale_dir_ar = os.path.join(os.getcwd(), 'locale', 'ar', 'LC_MESSAGES')
    os.makedirs(locale_dir_ar, exist_ok=True)
    output_mofile(translations_ar, os.path.join(locale_dir_ar, 'django.mo'))
    print("Compiled Arabic translations.")

    # French
    locale_dir_fr = os.path.join(os.getcwd(), 'locale', 'fr', 'LC_MESSAGES')
    os.makedirs(locale_dir_fr, exist_ok=True)
    output_mofile(translations_fr, os.path.join(locale_dir_fr, 'django.mo'))
    print("Compiled French translations.")
