#!/usr/bin/env python3
import os
import sys
from datetime import datetime
from pathlib import Path
import sqlite3
import json
import coverage

def analyze_coverage():
    """Analyze coverage data and generate a summary."""
    try:
        # Use coverage.py's API directly
        cov = coverage.Coverage()
        cov.load()
        
        results = []
        total_statements = 0
        total_missing = 0
        total_branches = 0
        total_missing_branches = 0
        
        # Get coverage data for each file
        for filename in cov.get_data().measured_files():
            if 'test' in filename or '__init__' in filename:
                continue
                
            analysis = cov._analyze(filename)
            
            statements = len(analysis.statements)
            missing = len(analysis.missing)
            branches = len(analysis.branch_lines()) if analysis.has_arcs() else 0
            missing_branches = len(analysis.missing_branch_arcs()) if analysis.has_arcs() else 0
            
            total_statements += statements
            total_missing += missing
            total_branches += branches
            total_missing_branches += missing_branches
            
            coverage_pct = (statements - missing) / statements * 100 if statements else 0
            clean_path = filename.replace('\\', '/').split('/')[-1]
            
            results.append({
                'file': clean_path,
                'coverage': coverage_pct,
                'statements': statements,
                'missing': missing,
                'branches': branches,
                'missing_branches': missing_branches
            })
            
        # Generate report
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\nTest Coverage Summary ({timestamp})")
        print("-" * 100)
        print(f"{'File':<30} {'Coverage':>10} {'Statements':>10} {'Missing':>10} {'Branches':>10} {'Miss Branch':>10}")
        print("-" * 100)
        
        for result in sorted(results, key=lambda x: x['coverage']):
            print(
                f"{result['file']:<30} "
                f"{result['coverage']:>10.1f}% "
                f"{result['statements']:>10d} "
                f"{result['missing']:>10d} "
                f"{result['branches']:>10d} "
                f"{result['missing_branches']:>10d}"
            )
            
        print("-" * 100)
        total_coverage = ((total_statements - total_missing) / total_statements * 100) if total_statements else 0
        print(
            f"{'Total':<30} "
            f"{total_coverage:>10.1f}% "
            f"{total_statements:>10d} "
            f"{total_missing:>10d} "
            f"{total_branches:>10d} "
            f"{total_missing_branches:>10d}"
        )
        
        branch_cov = ((total_branches - total_missing_branches) / total_branches * 100) if total_branches else 0
        print(f"\nBranch coverage: {branch_cov:.1f}% ({total_branches - total_missing_branches}/{total_branches})")
        
    except Exception as e:
        print(f"Error analyzing coverage: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    analyze_coverage()
