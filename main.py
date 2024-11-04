import pydicom as dicom
import matplotlib.pyplot as plt
import os


class DICOMViewer:
    def __init__(self, file_name):
        self.ds = dicom.dcmread(file_name)
        self.slices = self.ds.pixel_array
        self.current_slice = 0

        print(self.ds)

        self.num_slices = self.slices.shape[0] if self.slices.ndim == 3 else 1

        self.fig, self.ax = plt.subplots()
        self.ax.axis('off')
        self.image_display = self.ax.imshow(self.get_current_slice(), cmap='gray')
        self.ax.set_title(f'Slice {self.current_slice + 1}/{self.num_slices}')

        self.patient_name = self.ds.PatientName
        self.patient_id = self.ds.PatientID
        self.patient_birth_date = self.ds.get('PatientBirthDate', '(missing)')
        self.patient_sex = self.ds.get('PatientSex', '(missing)')

        self.display_patient_info()

        self.prev_button = plt.Button(plt.axes((0.1, 0.01, 0.1, 0.05)), 'Previous')
        self.next_button = plt.Button(plt.axes((0.8, 0.01, 0.1, 0.05)), 'Next')

        self.prev_button.on_clicked(self.show_previous_slice)
        self.next_button.on_clicked(self.show_next_slice)

        plt.show()

    def display_patient_info(self):
        infotext = f'Patient: {self.patient_name}\nID: {self.patient_id}\nBirth date: {self.patient_birth_date}\nPatient sex: {self.patient_sex}'
        self.ax.text(0.5, -0.03, infotext, ha='center', va='top', fontsize = 9, transform=self.ax.transAxes)

    def get_current_slice(self):
        return self.slices[self.current_slice] if self.slices.ndim == 3 else self.slices

    def update_image(self):
        self.image_display.set_array(self.get_current_slice())
        self.ax.set_title(f'Slice {self.current_slice + 1}/{self.num_slices}')
        self.fig.canvas.draw()

    def show_previous_slice(self, event):
        if self.current_slice > 0:
            self.current_slice -= 1
            self.update_image()

    def show_next_slice(self, event):
        if self.current_slice < self.num_slices - 1:
            self.current_slice += 1
            self.update_image()


def load_dicom_file():
    while True:
        try:
            file_name = input("Enter the name of the DICOM file (e.g., '0020.DCM'): ")

            if not os.path.exists(file_name):
                print("Error: File not found. Please check the file name and try again.")
                continue

            DICOMViewer(file_name)
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")


load_dicom_file()
