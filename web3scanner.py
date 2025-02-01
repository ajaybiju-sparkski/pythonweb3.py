import os
import subprocess
import json
import platform

def run_slither(contract_path):
    """Run Slither for static analysis."""
    report_file = "report.json"
    try:
        result = subprocess.run(
            ["slither", contract_path, "--json", report_file],
            capture_output=True, text=True
        )
        if os.path.exists(report_file):
            with open(report_file, "r") as file:
                report = json.load(file)
            return report
        else:
            return {"error": f"Slither output file not found: {report_file}"}
    except Exception as e:
        return {"error": f"Slither analysis failed: {str(e)}"}

def run_mythril(contract_path):
    """Run Mythril for symbolic execution."""
    try:
        result = subprocess.run(
            ["myth", "analyze", contract_path, "-o", "json"],
            capture_output=True, text=True
        )
        return json.loads(result.stdout) if result.stdout else {"error": "No Mythril output"}
    except Exception as e:
        return {"error": f"Mythril analysis failed: {str(e)}"}

def generate_report(slither_results, mythril_results):
    """Generate a security report from both analysis tools."""
    report = {
        "slither": slither_results,
        "mythril": mythril_results
    }
    with open("security_report.json", "w") as file:
        json.dump(report, file, indent=4)
    print("Security report generated: security_report.json")

def open_report():
    """Open the generated security report file."""
    try:
        if platform.system() == "Darwin":  
            subprocess.run(["open", "security_report.json"])
        elif platform.system() == "Windows":
            subprocess.run(["start", "security_report.json"], shell=True)
        else:  # Linux
            subprocess.run(["xdg-open", "security_report.json"])
    except FileNotFoundError:
        print("Security report file not found.")

def main():
    contract_path = input("Enter Solidity contract path: ")
    if not os.path.exists(contract_path):
        print("Error: Contract file not found!")
        return
    
    print("Running Slither...")
    slither_results = run_slither(contract_path)
    
    print("Running Mythril...")
    mythril_results = run_mythril(contract_path)
    
    generate_report(slither_results, mythril_results)
    print("Analysis complete. Check security_report.json for details.")
    
    open_report()

if __name__ == "__main__":
    main()
