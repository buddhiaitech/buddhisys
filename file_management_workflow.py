"""
File Management RPA Workflow
Automated file organization, cleanup, and management tasks
"""

import os
import sys
import time
import logging
import shutil
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
import json

class FileManagementWorkflow:
    def __init__(self):
        """Initialize File Management Workflow"""
        self.logger = self._setup_logging()
        self.workspace_dir = os.path.dirname(os.path.abspath(__file__))
        
    def _setup_logging(self):
        """Setup logging configuration"""
        logger = logging.getLogger('FileManagementWorkflow')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def create_sample_files(self):
        """Create sample files for demonstration"""
        try:
            self.logger.info("📁 Creating sample files...")
            
            # Create test directory structure
            test_dir = os.path.join(self.workspace_dir, 'logs', 'file_management_test')
            os.makedirs(test_dir, exist_ok=True)
            
            # Create subdirectories
            subdirs = ['documents', 'images', 'archives', 'temp', 'reports']
            for subdir in subdirs:
                os.makedirs(os.path.join(test_dir, subdir), exist_ok=True)
            
            # Create sample files with different extensions
            sample_files = [
                ('documents', 'report_2024.pdf', 'PDF document'),
                ('documents', 'contract.docx', 'Word document'),
                ('documents', 'presentation.pptx', 'PowerPoint presentation'),
                ('images', 'photo1.jpg', 'JPEG image'),
                ('images', 'screenshot.png', 'PNG image'),
                ('images', 'logo.svg', 'SVG image'),
                ('archives', 'backup.zip', 'ZIP archive'),
                ('temp', 'temp_file1.txt', 'Temporary text file'),
                ('temp', 'temp_file2.log', 'Log file'),
                ('reports', 'sales_report.xlsx', 'Excel report'),
                ('reports', 'analytics.json', 'JSON data file')
            ]
            
            created_files = []
            for subdir, filename, content in sample_files:
                file_path = os.path.join(test_dir, subdir, filename)
                with open(file_path, 'w') as f:
                    f.write(f"Sample {content} created at {datetime.now().isoformat()}")
                created_files.append(file_path)
            
            self.logger.info(f"✅ Created {len(created_files)} sample files in {test_dir}")
            return test_dir, created_files
            
        except Exception as e:
            self.logger.error(f"Error creating sample files: {e}")
            return None, []
    
    def organize_files_by_type(self, source_dir):
        """Organize files by their type/extension"""
        try:
            self.logger.info("🗂️ Organizing files by type...")
            
            # File type mappings
            file_types = {
                'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf'],
                'images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp'],
                'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
                'spreadsheets': ['.xlsx', '.xls', '.csv'],
                'presentations': ['.pptx', '.ppt'],
                'code': ['.py', '.js', '.html', '.css', '.json', '.xml'],
                'other': []
            }
            
            organized_count = 0
            
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    # Find appropriate category
                    category = 'other'
                    for cat, extensions in file_types.items():
                        if file_ext in extensions:
                            category = cat
                            break
                    
                    # Create category directory if it doesn't exist
                    category_dir = os.path.join(source_dir, 'organized', category)
                    os.makedirs(category_dir, exist_ok=True)
                    
                    # Move file to category directory
                    dest_path = os.path.join(category_dir, file)
                    if not os.path.exists(dest_path):
                        shutil.move(file_path, dest_path)
                        organized_count += 1
                        self.logger.info(f"📁 Moved {file} to {category}/")
            
            self.logger.info(f"✅ Organized {organized_count} files by type")
            return organized_count
            
        except Exception as e:
            self.logger.error(f"Error organizing files: {e}")
            return 0
    
    def cleanup_old_files(self, directory, days_old=30):
        """Clean up files older than specified days"""
        try:
            self.logger.info(f"🧹 Cleaning up files older than {days_old} days...")
            
            cutoff_date = datetime.now() - timedelta(days=days_old)
            cleaned_count = 0
            cleaned_files = []
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if file_time < cutoff_date:
                        try:
                            os.remove(file_path)
                            cleaned_count += 1
                            cleaned_files.append(file_path)
                            self.logger.info(f"🗑️ Removed old file: {file}")
                        except Exception as e:
                            self.logger.warning(f"Could not remove {file}: {e}")
            
            self.logger.info(f"✅ Cleaned up {cleaned_count} old files")
            return cleaned_count, cleaned_files
            
        except Exception as e:
            self.logger.error(f"Error cleaning up files: {e}")
            return 0, []
    
    def create_archive(self, source_dir, archive_name):
        """Create ZIP archive of directory"""
        try:
            self.logger.info(f"📦 Creating archive: {archive_name}")
            
            archive_path = os.path.join(self.workspace_dir, 'logs', f"{archive_name}.zip")
            os.makedirs(os.path.dirname(archive_path), exist_ok=True)
            
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname)
            
            # Get archive size
            archive_size = os.path.getsize(archive_path)
            size_mb = archive_size / (1024 * 1024)
            
            self.logger.info(f"✅ Archive created: {archive_path} ({size_mb:.2f} MB)")
            return archive_path
            
        except Exception as e:
            self.logger.error(f"Error creating archive: {e}")
            return None
    
    def generate_file_report(self, directory):
        """Generate comprehensive file analysis report"""
        try:
            self.logger.info("📊 Generating file analysis report...")
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'directory': directory,
                'total_files': 0,
                'total_size': 0,
                'file_types': {},
                'largest_files': [],
                'oldest_files': [],
                'newest_files': []
            }
            
            file_info = []
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        stat = os.stat(file_path)
                        file_size = stat.st_size
                        file_time = datetime.fromtimestamp(stat.st_mtime)
                        file_ext = os.path.splitext(file)[1].lower()
                        
                        file_info.append({
                            'name': file,
                            'path': file_path,
                            'size': file_size,
                            'modified': file_time.isoformat(),
                            'extension': file_ext
                        })
                        
                        report['total_files'] += 1
                        report['total_size'] += file_size
                        
                        # Count file types
                        if file_ext in report['file_types']:
                            report['file_types'][file_ext] += 1
                        else:
                            report['file_types'][file_ext] = 1
                            
                    except Exception as e:
                        self.logger.warning(f"Could not analyze {file}: {e}")
            
            # Sort files by size (largest first)
            file_info.sort(key=lambda x: x['size'], reverse=True)
            report['largest_files'] = file_info[:10]  # Top 10 largest
            
            # Sort files by modification time
            file_info.sort(key=lambda x: x['modified'])
            report['oldest_files'] = file_info[:5]  # 5 oldest
            report['newest_files'] = file_info[-5:]  # 5 newest
            
            # Convert total size to MB
            report['total_size_mb'] = report['total_size'] / (1024 * 1024)
            
            # Save report
            report_path = os.path.join(self.workspace_dir, 'logs', f'file_analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            self.logger.info(f"✅ File analysis report created: {report_path}")
            return report_path, report
            
        except Exception as e:
            self.logger.error(f"Error generating file report: {e}")
            return None, None
    
    def execute_file_management_workflow(self):
        """Execute the complete file management workflow"""
        try:
            self.logger.info("🚀 Starting File Management Workflow...")
            
            # Create sample files
            test_dir, created_files = self.create_sample_files()
            if not test_dir:
                return False
            
            self.logger.info(f"📁 Working with {len(created_files)} sample files")
            
            # Organize files by type
            organized_count = self.organize_files_by_type(test_dir)
            
            # Clean up old files (simulate with temp files)
            temp_dir = os.path.join(test_dir, 'temp')
            cleaned_count, cleaned_files = self.cleanup_old_files(temp_dir, days_old=0)  # Clean all temp files
            
            # Create archive of organized files
            organized_dir = os.path.join(test_dir, 'organized')
            if os.path.exists(organized_dir):
                archive_path = self.create_archive(organized_dir, f'organized_files_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            
            # Generate file analysis report
            report_path, report = self.generate_file_report(test_dir)
            
            if report:
                self.logger.info("📊 File Management Summary:")
                self.logger.info(f"   Total Files: {report['total_files']}")
                self.logger.info(f"   Total Size: {report['total_size_mb']:.2f} MB")
                self.logger.info(f"   File Types: {len(report['file_types'])}")
                self.logger.info(f"   Files Organized: {organized_count}")
                self.logger.info(f"   Files Cleaned: {cleaned_count}")
            
            self.logger.info("✅ File management workflow completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"File management workflow failed: {e}")
            return False

def main():
    """Main execution function"""
    print("📁 File Management RPA Workflow")
    print("=" * 50)
    print("This will organize files, clean up old files, and create archives!")
    print("=" * 50)
    
    # Check if running in non-interactive mode (API call)
    non_interactive = '--non-interactive' in sys.argv or os.getenv('NON_INTERACTIVE', '').lower() == 'true'
    
    if non_interactive:
        response = 'y'
        print("\n🤖 Running in non-interactive mode (API call)")
    else:
        # Ask for confirmation
        response = input("\nDo you want to start the file management workflow? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🚀 Starting File Management Workflow...")
        print("=" * 50)
        
        # Create and run automation
        automation = FileManagementWorkflow()
        success = automation.execute_file_management_workflow()
        
        if success:
            print("\n🎉 File Management Workflow completed successfully!")
            print("✅ Files organized, cleaned, and archived!")
        else:
            print("\n❌ File Management Workflow failed. Check logs for details.")
    else:
        print("\n❌ File management workflow cancelled.")

if __name__ == "__main__":
    main()
