import sys
from final_complete_workflow import FinalCompleteWorkflow


def main() -> int:
	wf = FinalCompleteWorkflow(headless=False)
	try:
		print("Setting up and visiting website...")
		ok = wf.step1_visit_website()
		print("Visit OK:" if ok else "Visit failed")

		print("Filling working PDF...")
		filled = wf.step2_fill_working_pdf()
		print("Filled PDF:", filled)
		return 0
	except Exception as e:
		print("Error:", e)
		return 1
	finally:
		wf.close()


if __name__ == "__main__":
	sys.exit(main())
