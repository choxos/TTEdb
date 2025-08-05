#!/usr/bin/env python3
"""
Script to clean up the analysis template by removing all old HTML/CSS forest plots
and keeping only the new Python/Plotly forest plots.
"""

def clean_analysis_template():
    """Remove all old HTML/CSS forest plot remnants"""
    
    # Read the current template
    with open('templates/ttedb/analysis.html', 'r') as f:
        content = f.read()
    
    # Find the Forest Plots tab end
    forest_tab_end = content.find('</div>\n\n        <!-- Outlier/Inlier Analysis Tab -->')
    if forest_tab_end == -1:
        # Look for alternative patterns
        forest_tab_end = content.find('        <!-- Outlier/Inlier Analysis Tab -->')
    
    if forest_tab_end == -1:
        print("❌ Could not find outlier-inlier tab start")
        return False
        
    # Find the Forest Plots tab start
    forest_tab_start = content.find('        <!-- Forest Plots Tab -->')
    if forest_tab_start == -1:
        print("❌ Could not find forest plots tab start")
        return False
    
    # Keep everything before Forest Plots tab
    before_forest = content[:forest_tab_start]
    
    # Add clean Forest Plots tab
    clean_forest_tab = '''        <!-- Forest Plots Tab -->
        <div class="tab-pane fade" id="forest" role="tabpanel">
            <!-- Include Latest Plotly JavaScript -->
            <script src="https://cdn.plot.ly/plotly-2.28.0.min.js"></script>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="alert alert-success mb-4">
                        <h5><i class="fa fa-chart-line me-2"></i>Interactive Forest Plots (Python/Plotly)</h5>
                        <p><strong>Professional forest plots with advanced tooltip management!</strong> These plots feature:</p>
                        <ul class="mb-0">
                            <li>✅ <strong>Perfect cursor-following tooltips</strong> with rich information</li>
                            <li>✅ <strong>Zoom and pan capabilities</strong> for detailed exploration</li>
                            <li>✅ <strong>All studies shown by default</strong> - no hidden data</li>
                            <li>✅ <strong>Automatic log/linear scaling</strong> for different measure types</li>
                            <li>✅ <strong>Professional statistical visualization</strong> with null effect lines</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- Hazard Ratio Forest Plot -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5><i class="fa fa-chart-line me-2"></i>Hazard Ratio Studies (n=67)</h5>
                    <small class="text-muted">Interactive Plotly visualization with log scale and advanced tooltips</small>
                </div>
                <div class="card-body">
                    {{ forest_plots.hr|safe }}
                </div>
            </div>
            
            <!-- Odds Ratio Forest Plot -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5><i class="fa fa-chart-line me-2"></i>Odds Ratio Studies (n=34)</h5>
                    <small class="text-muted">Interactive Plotly visualization with log scale and advanced tooltips</small>
                </div>
                <div class="card-body">
                    {{ forest_plots.or|safe }}
                </div>
            </div>
            
            <!-- Risk Ratio Forest Plot -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5><i class="fa fa-chart-line me-2"></i>Risk Ratio Studies (n=28)</h5>
                    <small class="text-muted">Interactive Plotly visualization with log scale and advanced tooltips</small>
                </div>
                <div class="card-body">
                    {{ forest_plots.rr|safe }}
                </div>
            </div>
            
            <!-- Risk Difference Forest Plot -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5><i class="fa fa-chart-line me-2"></i>Risk Difference Studies (n=19)</h5>
                    <small class="text-muted">Interactive Plotly visualization with linear scale and advanced tooltips</small>
                </div>
                <div class="card-body">
                    {{ forest_plots.rd|safe }}
                </div>
            </div>
            
            <!-- Mean Difference Forest Plot -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5><i class="fa fa-chart-line me-2"></i>Mean Difference Studies (n=23)</h5>
                    <small class="text-muted">Interactive Plotly visualization with linear scale and advanced tooltips</small>
                </div>
                <div class="card-body">
                    {{ forest_plots.md|safe }}
                </div>
            </div>
            
            <!-- Summary -->
            <div class="card">
                <div class="card-header">
                    <h5><i class="fa fa-info-circle me-2"></i>Python/Plotly Forest Plot Advantages</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>🎯 Perfect Tooltip Management</h6>
                            <ul>
                                <li>Tooltips follow cursor precisely</li>
                                <li>Rich, formatted hover information</li>
                                <li>No positioning issues or cutoffs</li>
                                <li>Professional statistical display</li>
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <h6>🔬 Advanced Interactivity</h6>
                            <ul>
                                <li>Zoom and pan for detailed analysis</li>
                                <li>Automatic axis scaling (log/linear)</li>
                                <li>Professional publication-quality plots</li>
                                <li>Export capabilities (PNG, SVG, HTML)</li>
                            </ul>
                        </div>
                    </div>
                    <div class="mt-3">
                        <small class="text-muted">
                            <strong>Technical Note:</strong> These forest plots are generated server-side using Python and Plotly, 
                            providing superior interactivity and tooltip management compared to HTML/CSS implementations.
                        </small>
                    </div>
                </div>
            </div>
        </div>

        '''
    
    # Find everything after the old forest plots content
    after_forest = content[forest_tab_end:]
    
    # Combine clean content
    clean_content = before_forest + clean_forest_tab + after_forest
    
    # Write the clean template
    with open('templates/ttedb/analysis.html', 'w') as f:
        f.write(clean_content)
    
    print("✅ Analysis template cleaned successfully!")
    print("✅ Removed all old HTML/CSS forest plot remnants")
    print("✅ Kept only Python/Plotly forest plots")
    return True

if __name__ == "__main__":
    success = clean_analysis_template()
    if success:
        print("\n🎯 Template is now clean and ready!")
        print("🔧 Don't forget to run VPS CSP fixes!")
    else:
        print("\n❌ Cleanup failed - manual intervention needed")