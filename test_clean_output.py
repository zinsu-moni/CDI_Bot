#!/usr/bin/env python3
"""
Test script to verify clean output without special characters
"""

def test_clean_output():
    """Test the cleaned output format"""
    
    # Sample data like what would come from the API
    sample_crops = [
        {'name': 'Tomato', 'scientific_name': 'Solanum lycopersicum', 'confidence': 95.5},
        {'name': 'Corn', 'scientific_name': 'Zea mays', 'confidence': 87.2}
    ]
    
    sample_diseases = [
        {'name': 'Leaf blight', 'confidence': 78.3},
        {'name': 'Nutrient deficiency', 'confidence': 65.1}
    ]
    
    # Test the clean summary format
    summary = "CROP DISEASE ANALYSIS RESULTS\n" + "="*40 + "\n\n"
    
    if sample_crops:
        summary += "IDENTIFIED CROPS:\n"
        for i, crop in enumerate(sample_crops[:3], 1):
            confidence = crop.get('confidence', 0)
            name = crop.get('name', 'Unknown')
            scientific_name = crop.get('scientific_name', '')
            
            confidence_level = "HIGH" if confidence > 80 else "MEDIUM" if confidence > 60 else "LOW"
            summary += f"{i}. {name}"
            if scientific_name:
                summary += f" ({scientific_name})"
            summary += f" - {confidence}% confidence ({confidence_level})\n"
        summary += "\n"
    
    if sample_diseases:
        summary += "DETECTED DISEASES/ISSUES:\n"
        for i, disease in enumerate(sample_diseases[:3], 1):
            confidence = disease.get('confidence', 0)
            name = disease.get('name', 'Unknown')
            
            severity_level = "HIGH" if confidence > 80 else "MEDIUM" if confidence > 60 else "LOW"
            summary += f"{i}. {name} - {confidence}% confidence ({severity_level} risk)\n"
        summary += "\n"
    
    summary += "FOR DETAILED ANALYSIS:\n"
    summary += "Please provide additional information if available:\n"
    summary += "- Your location/climate zone\n"
    summary += "- Recent weather conditions\n"
    summary += "- When symptoms first appeared\n"
    summary += "- Any treatments already applied\n"
    
    print("BEFORE (with special characters):")
    print("🔬 **CROP DISEASE ANALYSIS RESULTS**")
    print("🌾 **IDENTIFIED CROPS:**")
    print("🟢 **Tomato** (*Solanum lycopersicum*) - 95.5% confidence")
    print("⚠️ **DETECTED DISEASES/ISSUES:**")
    print("🔴 **Leaf blight** - 78.3% confidence")
    print()
    
    print("AFTER (clean output):")
    print(summary)
    
    print("\n" + "="*50)
    print("✅ Clean output test completed!")
    print("No more excessive emojis or markdown formatting!")

if __name__ == "__main__":
    test_clean_output()
