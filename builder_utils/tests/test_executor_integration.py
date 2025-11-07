#!/usr/bin/env python3
"""
Example script showing how Claude Code can use py_ex.py to test visualizations
"""

import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_ex import FileExecutor
import json

def test_skill_visualization_with_executor(skill_file_path: str, skill_name: str):
    """
    Example of how Claude Code can test visualizations using the executor
    
    Args:
        skill_file_path: Path to the skill file to test
        skill_name: Name of the skill function
    """
    
    # Create the test script content
    test_script = f'''
# Auto-generated visualization test script
import sys
sys.path.append('.')

from viz_previewer import quick_json_validation, test_skill_visualization_standalone
import json

# Test the skill visualization
print("🧪 Starting visualization test...")

# First, quick JSON validation (no browser needed)
print("📝 Step 1: JSON Structure Validation")
json_result = quick_json_validation("{skill_file_path}", "{skill_name}")
print(f"JSON Test Result: {{json_result['test_summary']}}")

if json_result["errors"]:
    print("❌ JSON Validation Errors:")
    for error in json_result["errors"]:
        print(f"  - {{error}}")

if json_result["warnings"]:
    print("⚠️ JSON Validation Warnings:")
    for warning in json_result["warnings"]:
        print(f"  - {{warning}}")

# If JSON is valid, run full browser test
if json_result["success"]:
    print("\\n🌐 Step 2: Full Browser Test (with temporary files)")
    try:
        full_result = test_skill_visualization_standalone("{skill_file_path}", "{skill_name}", headless=True)
        print(f"Full Test Result: {{full_result['test_summary']}}")

        if full_result["errors"]:
            print("❌ Browser Test Errors:")
            for error in full_result["errors"]:
                print(f"  - {{error}}")

        if full_result["warnings"]:
            print("⚠️ Browser Test Warnings:")
            for warning in full_result["warnings"]:
                print(f"  - {{warning}}")

        if full_result["performance_metrics"]:
            print("📈 Performance Metrics:")
            for key, value in full_result["performance_metrics"].items():
                print(f"  {{key}}: {{value}}")

        # Output final result as JSON for easy parsing
        print("\\n" + "="*50)
        print("FINAL_RESULT_JSON:")
        print(json.dumps(full_result, indent=2))

    except Exception as e:
        print(f"❌ Browser test failed: {{e}}")
        print("\\nFINAL_RESULT_JSON:")
        print(json.dumps({{"success": False, "errors": [f"Browser test failed: {{e}}"], "test_summary": "Browser test failed"}}, indent=2))
else:
    print("\\n⏭️ Skipping browser test due to JSON validation failures")
    print("\\nFINAL_RESULT_JSON:")
    print(json.dumps(json_result, indent=2))

print("\\n✅ Visualization test completed")
'''
    
    # Write the test script to a temporary file
    test_file_path = f"temp_viz_test_{skill_name}.py"
    with open(test_file_path, 'w') as f:
        f.write(test_script)
    
    print(f"📝 Created test script: {test_file_path}")
    
    # Execute the test using FileExecutor
    executor = FileExecutor()
    print(f"🚀 Executing visualization test for {skill_name}...")
    
    result = executor.run_file(test_file_path)
    
    # Clean up the temporary file
    import os
    try:
        os.remove(test_file_path)
    except:
        pass
    
    # Parse and return results
    output = result.get('stdout', '')
    errors = result.get('stderr', '')
    
    print("📊 Test Execution Results:")
    print("=" * 50)
    print(output)
    
    if errors:
        print("\n❌ Execution Errors:")
        print(errors)
    
    # Try to extract the JSON result
    try:
        if "FINAL_RESULT_JSON:" in output:
            json_start = output.find("FINAL_RESULT_JSON:") + len("FINAL_RESULT_JSON:")
            json_part = output[json_start:].strip()
            # Find the JSON object
            lines = json_part.split('\n')
            json_lines = []
            in_json = False
            brace_count = 0
            
            for line in lines:
                if line.strip().startswith('{'):
                    in_json = True
                    brace_count += line.count('{') - line.count('}')
                    json_lines.append(line)
                elif in_json:
                    brace_count += line.count('{') - line.count('}')
                    json_lines.append(line)
                    if brace_count <= 0:
                        break
            
            if json_lines:
                json_str = '\n'.join(json_lines)
                test_result = json.loads(json_str)
                return test_result
    except Exception as e:
        print(f"⚠️ Could not parse JSON result: {e}")
    
    # Fallback result
    return {
        "success": "✅" in output and "❌" not in output,
        "output": output,
        "errors": errors.split('\n') if errors else [],
        "test_summary": "Test completed - check output for details"
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 3:
        skill_file = sys.argv[1]
        skill_name = sys.argv[2]
        
        print(f"🧪 Testing {skill_name} from {skill_file}")
        result = test_skill_visualization_with_executor(skill_file, skill_name)
        
        print(f"\n🎯 Final Result: {result.get('test_summary', 'Unknown')}")
        if result.get('success'):
            print("✅ PASSED")
        else:
            print("❌ FAILED")
            
    else:
        print("Usage: python test_viz_with_executor.py <skill_file.py> <skill_function_name>")
        print("Example: python test_viz_with_executor.py competitive_brand_analysis.py competitive_brand_analysis")
