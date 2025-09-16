"""
Data Processing RPA Workflow
Automated data processing, Excel manipulation, and file management
"""

import os
import sys
import time
import logging
import pandas as pd
import openpyxl
from datetime import datetime
from pathlib import Path
import json

class DataProcessingWorkflow:
    def __init__(self):
        """Initialize Data Processing Workflow"""
        self.logger = self._setup_logging()
        self.workspace_dir = os.path.dirname(os.path.abspath(__file__))
        
    def _setup_logging(self):
        """Setup logging configuration"""
        logger = logging.getLogger('DataProcessingWorkflow')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def create_sample_data(self):
        """Create sample data for processing"""
        try:
            self.logger.info("📊 Creating sample data...")
            
            # Create sample sales data
            sales_data = {
                'Date': pd.date_range('2024-01-01', periods=100, freq='D'),
                'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'] * 20,
                'Quantity': [1, 2, 1, 1, 1] * 20,
                'Price': [999.99, 29.99, 79.99, 299.99, 149.99] * 20,
                'Customer': [f'Customer_{i%10}' for i in range(100)],
                'Region': ['North', 'South', 'East', 'West'] * 25
            }
            
            df = pd.DataFrame(sales_data)
            df['Total'] = df['Quantity'] * df['Price']
            
            # Save to CSV
            csv_path = os.path.join(self.workspace_dir, 'logs', 'sample_sales_data.csv')
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            df.to_csv(csv_path, index=False)
            
            self.logger.info(f"✅ Sample data created: {csv_path}")
            return csv_path
            
        except Exception as e:
            self.logger.error(f"Error creating sample data: {e}")
            return None
    
    def process_sales_data(self, csv_path):
        """Process and analyze sales data"""
        try:
            self.logger.info("📈 Processing sales data...")
            
            # Read CSV data
            df = pd.read_csv(csv_path)
            
            # Data analysis
            analysis = {
                'total_sales': df['Total'].sum(),
                'average_order_value': df['Total'].mean(),
                'total_orders': len(df),
                'top_product': df['Product'].value_counts().index[0],
                'top_region': df['Region'].value_counts().index[0],
                'date_range': f"{df['Date'].min()} to {df['Date'].max()}"
            }
            
            # Create summary by product
            product_summary = df.groupby('Product').agg({
                'Quantity': 'sum',
                'Total': 'sum',
                'Price': 'mean'
            }).round(2)
            
            # Create summary by region
            region_summary = df.groupby('Region').agg({
                'Total': 'sum',
                'Quantity': 'sum'
            }).round(2)
            
            # Create monthly summary
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.to_period('M')
            monthly_summary = df.groupby('Month').agg({
                'Total': 'sum',
                'Quantity': 'sum'
            }).round(2)
            
            self.logger.info("✅ Sales data processed successfully")
            
            return {
                'analysis': analysis,
                'product_summary': product_summary,
                'region_summary': region_summary,
                'monthly_summary': monthly_summary
            }
            
        except Exception as e:
            self.logger.error(f"Error processing sales data: {e}")
            return None
    
    def create_excel_report(self, data, output_path):
        """Create comprehensive Excel report"""
        try:
            self.logger.info("📋 Creating Excel report...")
            
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Summary sheet
                summary_df = pd.DataFrame(list(data['analysis'].items()), 
                                        columns=['Metric', 'Value'])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Product summary
                data['product_summary'].to_excel(writer, sheet_name='Products')
                
                # Region summary
                data['region_summary'].to_excel(writer, sheet_name='Regions')
                
                # Monthly summary
                data['monthly_summary'].to_excel(writer, sheet_name='Monthly')
                
                # Format the Excel file
                workbook = writer.book
                
                # Format summary sheet
                summary_sheet = workbook['Summary']
                for column in summary_sheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    summary_sheet.column_dimensions[column_letter].width = adjusted_width
            
            self.logger.info(f"✅ Excel report created: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating Excel report: {e}")
            return False
    
    def generate_json_report(self, data, output_path):
        """Generate JSON report for API consumption"""
        try:
            self.logger.info("📄 Generating JSON report...")
            
            # Convert DataFrames to dictionaries
            report = {
                'analysis': data['analysis'],
                'product_summary': data['product_summary'].to_dict(),
                'region_summary': data['region_summary'].to_dict(),
                'monthly_summary': data['monthly_summary'].to_dict(),
                'generated_at': datetime.now().isoformat(),
                'workflow': 'Data Processing RPA'
            }
            
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            self.logger.info(f"✅ JSON report created: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating JSON report: {e}")
            return False
    
    def execute_data_processing_workflow(self):
        """Execute the complete data processing workflow"""
        try:
            self.logger.info("🚀 Starting Data Processing Workflow...")
            
            # Create sample data
            csv_path = self.create_sample_data()
            if not csv_path:
                return False
            
            # Process the data
            processed_data = self.process_sales_data(csv_path)
            if not processed_data:
                return False
            
            # Create output directory
            output_dir = os.path.join(self.workspace_dir, 'logs')
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Create Excel report
            excel_path = os.path.join(output_dir, f'data_analysis_report_{timestamp}.xlsx')
            self.create_excel_report(processed_data, excel_path)
            
            # Create JSON report
            json_path = os.path.join(output_dir, f'data_analysis_report_{timestamp}.json')
            self.generate_json_report(processed_data, json_path)
            
            # Print summary
            analysis = processed_data['analysis']
            self.logger.info("📊 Data Processing Summary:")
            self.logger.info(f"   Total Sales: ${analysis['total_sales']:,.2f}")
            self.logger.info(f"   Average Order Value: ${analysis['average_order_value']:,.2f}")
            self.logger.info(f"   Total Orders: {analysis['total_orders']}")
            self.logger.info(f"   Top Product: {analysis['top_product']}")
            self.logger.info(f"   Top Region: {analysis['top_region']}")
            
            self.logger.info("✅ Data processing workflow completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Data processing workflow failed: {e}")
            return False

def main():
    """Main execution function"""
    print("📊 Data Processing RPA Workflow")
    print("=" * 50)
    print("This will process data, create reports, and generate insights!")
    print("=" * 50)
    
    # Check if running in non-interactive mode (API call)
    non_interactive = '--non-interactive' in sys.argv or os.getenv('NON_INTERACTIVE', '').lower() == 'true'
    
    if non_interactive:
        response = 'y'
        print("\n🤖 Running in non-interactive mode (API call)")
    else:
        # Ask for confirmation
        response = input("\nDo you want to start the data processing workflow? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🚀 Starting Data Processing Workflow...")
        print("=" * 50)
        
        # Create and run automation
        automation = DataProcessingWorkflow()
        success = automation.execute_data_processing_workflow()
        
        if success:
            print("\n🎉 Data Processing Workflow completed successfully!")
            print("✅ Reports generated and saved!")
        else:
            print("\n❌ Data Processing Workflow failed. Check logs for details.")
    else:
        print("\n❌ Data processing workflow cancelled.")

if __name__ == "__main__":
    main()
