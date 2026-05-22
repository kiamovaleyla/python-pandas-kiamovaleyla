import pandas as pd
from Medical_Devices import(
    MedicalDevices
)


def main():
    """Вход в программу."""

    worker = MedicalDevices('medical_diagnostic_devices_10000')

    # Correct form
    worker.correct_dates(['install_date', 'warranty_until', 'last_calibration_date', 'last_service_date'])
    worker.correct_status('status')

    # Warranty
    sorted_warranty = worker.df.sort_values(['warranty_until'])

    actual_warranties = sorted_warranty[sorted_warranty['warranty_until'] >= worker.time]
    non_actual_warranties = sorted_warranty[sorted_warranty['warranty_until'] < worker.time]

    # Problems

    problems = worker.df.groupby(["clinic_id", "clinic_name"], as_index=False).agg(
        issues_reported_12mo=('issues_reported_12mo', 'sum')
    )
    problems = problems.sort_values(['issues_reported_12mo'], ascending=False)

    # Calibration
    calibration_report = worker.calibrations_sheet()

    # Summary Table
    summary_table = worker.get_summary_table()

    with pd.ExcelWriter('Devices_prikol4ik.xlsx') as writer:
        worker.df.to_excel(writer, index=False, sheet_name='Medical_Devices')
        actual_warranties.to_excel(writer, index=False, sheet_name='Actual_Warranties')
        non_actual_warranties.to_excel(writer, index=False, sheet_name='Non-Actual_Warranties')
        problems.to_excel(writer, index=False, sheet_name='Problems')
        calibration_report.to_excel(writer, index=False, sheet_name='Calibration_Report')
        summary_table.to_excel(writer, index=False, sheet_name='Summary_Table')

main()