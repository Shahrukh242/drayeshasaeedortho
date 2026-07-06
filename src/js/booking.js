/* 
========================================================================
   DR. AYESHA SAEED PEDIATRIC ORTHOPEDICS - BOOKING JAVASCRIPT
   Handles: Booking Modal, Hospital Selection, Form Validation, Success Popups
========================================================================
*/

document.addEventListener('DOMContentLoaded', () => {

    // 1. MODAL TRIGGERS
    const bookingModal = document.getElementById('bookingModal');
    const closeBookingModal = document.getElementById('closeBookingModal');
    const bookButtons = document.querySelectorAll('.btn-book-trigger');
    const successModal = document.getElementById('successModal');
    const btnDismissSuccess = document.getElementById('btnDismissSuccess');

    const openModal = () => {
        bookingModal.classList.add('open');
        document.body.style.overflow = 'hidden';
        
        // Pre-fill default date to tomorrow
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const dateInput = document.getElementById('modalPreferredDate');
        if (dateInput) {
            dateInput.value = tomorrow.toISOString().split('T')[0];
            dateInput.min = tomorrow.toISOString().split('T')[0]; // Disable past dates
        }
    };

    const closeModal = () => {
        bookingModal.classList.remove('open');
        document.body.style.overflow = '';
    };

    bookButtons.forEach(btn => {
        btn.addEventListener('click', openModal);
    });

    if (closeBookingModal) {
        closeBookingModal.addEventListener('click', closeModal);
    }

    if (bookingModal) {
        // Close modal when clicking outside content
        bookingModal.addEventListener('click', (e) => {
            if (e.target === bookingModal) {
                closeModal();
            }
        });
    }

    if (btnDismissSuccess && successModal) {
        btnDismissSuccess.addEventListener('click', () => {
            successModal.classList.remove('open');
            document.body.style.overflow = '';
        });
    }

    // 2. HOSPITAL RADIO CARD SELECTORS (MODAL, INLINE, CONTACT FORMS)
    const setupHospitalRadios = (containerSelector, optionClass) => {
        const container = document.querySelector(containerSelector);
        if (!container) return;

        const options = container.querySelectorAll('.' + optionClass);
        options.forEach(option => {
            option.addEventListener('click', () => {
                // Deselect all options in this group
                options.forEach(opt => opt.classList.remove('selected'));
                // Select current
                option.classList.add('selected');
                
                const radio = option.querySelector('input[type="radio"]');
                if (radio) {
                    radio.checked = true;
                }
            });
        });
    };

    setupHospitalRadios('.booking-modal .hospital-select-container', 'hospital-option');
    setupHospitalRadios('#inlineBookingForm .hospital-select-container', 'hospital-option');
    setupHospitalRadios('#contactBookingForm .hospital-select-container', 'hospital-option');


    // 3. SET DATE PICKER CONSTRAINTS ON GENERAL FORMS
    const constrainDatePicker = (inputId) => {
        const dateInput = document.getElementById(inputId);
        if (dateInput) {
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            dateInput.value = tomorrow.toISOString().split('T')[0];
            dateInput.min = tomorrow.toISOString().split('T')[0];
        }
    };

    constrainDatePicker('preferredDate');
    constrainDatePicker('contactPreferredDate');


    // 4. GENERAL FORM VALIDATION AND PROCESSING
    const validateAndProcessForm = (formElement, fieldsMap) => {
        if (!formElement) return;

        formElement.addEventListener('submit', (e) => {
            e.preventDefault();

            // Fetch Fields
            const parentName = document.getElementById(fieldsMap.parentName).value.trim();
            const phone = document.getElementById(fieldsMap.phone).value.trim();
            const email = document.getElementById(fieldsMap.email).value.trim();
            const childName = document.getElementById(fieldsMap.childName).value.trim();
            const childAge = parseInt(document.getElementById(fieldsMap.childAge).value.trim(), 10);
            const medicalConcern = document.getElementById(fieldsMap.medicalConcern).value;
            const preferredDate = document.getElementById(fieldsMap.preferredDate).value;
            const preferredTime = document.getElementById(fieldsMap.preferredTime).value;
            const message = fieldsMap.message ? document.getElementById(fieldsMap.message).value.trim() : "";

            // Get selected hospital radio
            const hospitalRadio = formElement.querySelector('input[type="radio"]:checked');
            const preferredHospital = hospitalRadio ? hospitalRadio.value : "Medicare Karachi";

            // Basic Validation Check
            if (!parentName || !phone || !email || !childName || isNaN(childAge) || !medicalConcern || !preferredDate || !preferredTime) {
                alert("Please fill out all required fields marked with *");
                return;
            }

            // Child Age Constraint
            if (childAge < 0 || childAge > 18) {
                alert("Please enter a valid child's age between 0 and 18 years.");
                return;
            }

            // Phone Validation
            const phoneRegex = /^[+]?[0-9\s-]{10,15}$/;
            if (!phoneRegex.test(phone)) {
                alert("Please enter a valid contact phone number (e.g. +92 300 1234567)");
                return;
            }

            // Date validation (should not be past)
            const selectedDate = new Date(preferredDate);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            if (selectedDate < today) {
                alert("Preferred appointment date cannot be in the past.");
                return;
            }

            // Save to Local Storage for demonstration
            const appointmentRequest = {
                id: 'APT-' + Date.now(),
                parentName,
                phone,
                email,
                childName,
                childAge,
                medicalConcern,
                preferredHospital,
                preferredDate,
                preferredTime,
                message,
                status: 'Pending Coordinator Review',
                submittedAt: new Date().toISOString()
            };

            // Read existing, add, write back
            let existingAppointments = JSON.parse(localStorage.getItem('doctorAppointments') || '[]');
            existingAppointments.push(appointmentRequest);
            localStorage.setItem('doctorAppointments', JSON.stringify(existingAppointments));

            // Log submission
            console.log("Appointment Request Registered:", appointmentRequest);

            // Close Booking Modal if open
            closeModal();

            // Populate Success Dialog
            document.getElementById('summaryChildName').textContent = childName;
            document.getElementById('summaryHospital').textContent = preferredHospital;
            document.getElementById('summaryDate').textContent = preferredDate;
            document.getElementById('summaryTime').textContent = preferredTime;

            // Trigger Success Modal
            successModal.classList.add('open');
            document.body.style.overflow = 'hidden';

            // Reset current form fields
            formElement.reset();
            
            // Re-apply tomorrow's date baseline
            constrainDatePicker(fieldsMap.preferredDate);
        });
    };

    // Initialize individual forms
    validateAndProcessForm(document.getElementById('modalBookingForm'), {
        parentName: 'modalParentName',
        phone: 'modalPhoneNumber',
        email: 'modalEmail',
        childName: 'modalChildName',
        childAge: 'modalChildAge',
        medicalConcern: 'modalMedicalConcern',
        preferredDate: 'modalPreferredDate',
        preferredTime: 'modalPreferredTime',
        message: 'modalMessage'
    });

    validateAndProcessForm(document.getElementById('inlineBookingForm'), {
        parentName: 'parentName',
        phone: 'phoneNumber',
        email: 'email',
        childName: 'childName',
        childAge: 'childAge',
        medicalConcern: 'medicalConcern',
        preferredDate: 'preferredDate',
        preferredTime: 'preferredTime',
        message: 'message'
    });

    validateAndProcessForm(document.getElementById('contactBookingForm'), {
        parentName: 'contactParentName',
        phone: 'contactPhoneNumber',
        email: 'contactEmail',
        childName: 'contactChildName',
        childAge: 'contactChildAge',
        medicalConcern: 'contactMedicalConcern',
        preferredDate: 'contactPreferredDate',
        preferredTime: 'contactPreferredTime'
    });
});
