// Carbonic Documentation - Extra JavaScript

// Add structured data for better SEO
document.addEventListener('DOMContentLoaded', function() {
    // Add JSON-LD structured data for the library
    const structuredData = {
        "@context": "https://schema.org",
        "@type": "SoftwareLibrary",
        "name": "Carbonic",
        "description": "Modern Python datetime library with fluent API, timezone conversion, and comprehensive localization",
        "programmingLanguage": "Python",
        "codeRepository": "https://github.com/marepilc/carbonic",
        "downloadUrl": "https://pypi.org/project/carbonic/",
        "author": {
            "@type": "Person",
            "name": "Marek Pilczuk"
        },
        "license": "MIT",
        "keywords": ["python", "datetime", "timezone", "immutable", "fluent-api", "carbon"],
        "operatingSystem": "Cross-platform",
        "applicationCategory": "DeveloperApplication"
    };

    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(structuredData);
    document.head.appendChild(script);
});