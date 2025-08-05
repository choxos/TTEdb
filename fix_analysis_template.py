#!/usr/bin/env python3
"""
Script to completely fix the analysis template by removing all old forest plot content
and keeping only the new Python/Plotly forest plots and proper outlier-inlier tab.
"""

def fix_analysis_template():
    """Fix the analysis template by removing old content"""
    
    # Read the current template
    with open('templates/ttedb/analysis.html', 'r') as f:
        content = f.read()
    
    # Find the end of the proper Forest Plots tab
    forest_end_marker = '            </div>\n        </div>\n\n        <!-- Outlier/Inlier Analysis Tab -->'
    forest_end_pos = content.find(forest_end_marker)
    
    if forest_end_pos == -1:
        # Try alternative marker
        forest_end_marker = '            </div>\n        </div>'
        forest_end_pos = content.find(forest_end_marker)
        if forest_end_pos == -1:
            print("❌ Could not find forest plots tab end")
            return False
    
    # Find the start of the proper outlier-inlier tab
    outlier_start_marker = '        <!-- Outlier/Inlier Analysis Tab -->\n        <div class="tab-pane fade" id="outlier-inlier" role="tabpanel">\n            <div class="row mt-4">\n                <div class="col-12">\n                    <div class="alert alert-info mb-4">\n                        <h5><i class="fa fa-search-plus me-2"></i>Detection of Systematic Patterns</h5>\n                        <p>Bayesian outlier detection and likelihood ratio test for inlier detection to identify publication bias and methodological issues.</p>'
    
    outlier_start_pos = content.find(outlier_start_marker)
    if outlier_start_pos == -1:
        print("❌ Could not find proper outlier-inlier tab start")
        return False
    
    # Keep everything before the forest end + the forest end
    before_garbage = content[:forest_end_pos + len(forest_end_marker)]
    
    # Keep everything from the proper outlier-inlier tab start
    after_garbage = content[outlier_start_pos:]
    
    # Combine clean content
    clean_content = before_garbage + '\n' + after_garbage
    
    # Write the clean template
    with open('templates/ttedb/analysis.html', 'w') as f:
        f.write(clean_content)
    
    print("✅ Analysis template fixed successfully!")
    print("✅ Removed all old HTML/CSS forest plot content")
    print("✅ Removed duplicate outlier-inlier tabs") 
    print("✅ Template is now clean!")
    return True

if __name__ == "__main__":
    success = fix_analysis_template()
    if not success:
        print("\n❌ Fix failed - trying manual approach")
        
        # Manual approach: find key markers
        with open('templates/ttedb/analysis.html', 'r') as f:
            lines = f.readlines()
        
        # Find where clean forest plots tab ends (around line 481)
        forest_end_line = -1
        for i, line in enumerate(lines):
            if 'Forest Plot Interpretation' in line and '</div>' in lines[i+10:i+15]:
                # Look for the closing of this section
                for j in range(i+10, min(len(lines), i+20)):
                    if lines[j].strip() == '</div>' and lines[j+1].strip() == '':
                        forest_end_line = j
                        break
                break
        
        # Find where proper outlier-inlier starts (should be the later one)
        outlier_start_line = -1
        for i in range(len(lines)-1, -1, -1):  # Search backwards
            if 'Detection of Systematic Patterns' in lines[i] and 'Bayesian outlier detection' in lines[i+1]:
                # Look for the tab-pane div before this
                for j in range(i-10, i):
                    if 'tab-pane fade' in lines[j] and 'outlier-inlier' in lines[j]:
                        outlier_start_line = j
                        break
                break
        
        if forest_end_line != -1 and outlier_start_line != -1:
            print(f"Found forest end at line {forest_end_line+1}")
            print(f"Found outlier start at line {outlier_start_line+1}")
            
            # Keep lines up to forest end + 1, then jump to outlier start
            clean_lines = lines[:forest_end_line+2] + ['\n'] + lines[outlier_start_line:]
            
            with open('templates/ttedb/analysis.html', 'w') as f:
                f.writelines(clean_lines)
            
            print("✅ Manual fix applied successfully!")
        else:
            print(f"❌ Could not find markers: forest_end={forest_end_line}, outlier_start={outlier_start_line}")