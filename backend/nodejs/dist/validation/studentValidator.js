"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.handleValidationErrors = exports.validateStudentInput = void 0;
const express_validator_1 = require("express-validator");
/**
 * Validation rules for student record input
 */
exports.validateStudentInput = [
    (0, express_validator_1.body)('student.institution_type')
        .optional()
        .isIn(['Federal', 'State', 'Private'])
        .withMessage('institution_type must be one of: Federal, State, Private'),
    (0, express_validator_1.body)('student.faculty')
        .optional()
        .isString()
        .trim()
        .isLength({ min: 1, max: 100 })
        .withMessage('faculty must be a non-empty string up to 100 characters'),
    (0, express_validator_1.body)('student.department')
        .optional()
        .isString()
        .trim()
        .isLength({ min: 1, max: 100 })
        .withMessage('department must be a non-empty string up to 100 characters'),
    (0, express_validator_1.body)('student.level')
        .optional()
        .isInt({ min: 100, max: 500 })
        .withMessage('level must be an integer between 100 and 500'),
    (0, express_validator_1.body)('student.entry_mode')
        .optional()
        .isIn(['UTME', 'DirectEntry', 'Transfer'])
        .withMessage('entry_mode must be one of: UTME, DirectEntry, Transfer'),
    (0, express_validator_1.body)('student.age')
        .optional()
        .isInt({ min: 15, max: 65 })
        .withMessage('age must be an integer between 15 and 65'),
    (0, express_validator_1.body)('student.sex')
        .optional()
        .isIn(['Male', 'Female'])
        .withMessage('sex must be either Male or Female'),
    (0, express_validator_1.body)('student.state_of_origin')
        .optional()
        .isString()
        .trim()
        .isLength({ min: 2, max: 50 })
        .withMessage('state_of_origin must be a string between 2 and 50 characters'),
    (0, express_validator_1.body)('student.residency_status')
        .optional()
        .isIn(['OnCampus', 'OffCampus'])
        .withMessage('residency_status must be either OnCampus or OffCampus'),
    (0, express_validator_1.body)('student.socioeconomic_band')
        .optional()
        .isIn(['Low', 'Middle', 'High'])
        .withMessage('socioeconomic_band must be one of: Low, Middle, High'),
    (0, express_validator_1.body)('student.utme_score')
        .optional()
        .isInt({ min: 0, max: 400 })
        .withMessage('utme_score must be an integer between 0 and 400'),
    (0, express_validator_1.body)('student.post_utme_score')
        .optional()
        .isFloat({ min: 0, max: 100 })
        .withMessage('post_utme_score must be a number between 0 and 100'),
    (0, express_validator_1.body)('student.entry_qualification')
        .optional()
        .isIn(['SSCE', 'ND', 'HND', 'Alevel'])
        .withMessage('entry_qualification must be one of: SSCE, ND, HND, Alevel'),
    (0, express_validator_1.body)('student.prev_semester_gpa')
        .optional()
        .isFloat({ min: 0, max: 5 })
        .withMessage('prev_semester_gpa must be a number between 0 and 5'),
    (0, express_validator_1.body)('student.cumulative_cgpa')
        .optional()
        .isFloat({ min: 0, max: 5 })
        .withMessage('cumulative_cgpa must be a number between 0 and 5'),
    (0, express_validator_1.body)('student.carryover_courses_count')
        .optional()
        .isInt({ min: 0 })
        .withMessage('carryover_courses_count must be a non-negative integer'),
    (0, express_validator_1.body)('student.failed_courses_prev_semester')
        .optional()
        .isInt({ min: 0 })
        .withMessage('failed_courses_prev_semester must be a non-negative integer'),
    (0, express_validator_1.body)('student.core_courses_failed_total')
        .optional()
        .isInt({ min: 0 })
        .withMessage('core_courses_failed_total must be a non-negative integer'),
    (0, express_validator_1.body)('student.course_load_units')
        .optional()
        .isInt({ min: 0 })
        .withMessage('course_load_units must be a non-negative integer'),
    (0, express_validator_1.body)('student.continuous_assessment_avg')
        .optional()
        .isFloat({ min: 0, max: 40 })
        .withMessage('continuous_assessment_avg must be a number between 0 and 40'),
    (0, express_validator_1.body)('student.attendance_rate')
        .optional()
        .isFloat({ min: 0, max: 1 })
        .withMessage('attendance_rate must be a number between 0 and 1'),
    (0, express_validator_1.body)('student.library_visits_per_month')
        .optional()
        .isInt({ min: 0 })
        .withMessage('library_visits_per_month must be a non-negative integer'),
    (0, express_validator_1.body)('student.lms_logins_per_week')
        .optional()
        .isInt({ min: 0 })
        .withMessage('lms_logins_per_week must be a non-negative integer'),
    (0, express_validator_1.body)('student.assignment_submission_rate')
        .optional()
        .isFloat({ min: 0, max: 1 })
        .withMessage('assignment_submission_rate must be a number between 0 and 1'),
    (0, express_validator_1.body)('student.late_registration_flag')
        .optional()
        .isInt({ min: 0, max: 1 })
        .withMessage('late_registration_flag must be 0 or 1'),
    (0, express_validator_1.body)('student.financial_clearance_delay_days')
        .optional()
        .isInt({ min: 0 })
        .withMessage('financial_clearance_delay_days must be a non-negative integer'),
    (0, express_validator_1.body)('student.disciplinary_case_flag')
        .optional()
        .isInt({ min: 0, max: 1 })
        .withMessage('disciplinary_case_flag must be 0 or 1'),
    (0, express_validator_1.body)('student.counselling_visits_semester')
        .optional()
        .isInt({ min: 0 })
        .withMessage('counselling_visits_semester must be a non-negative integer'),
    (0, express_validator_1.body)('student.medical_leave_flag')
        .optional()
        .isInt({ min: 0, max: 1 })
        .withMessage('medical_leave_flag must be 0 or 1'),
];
/**
 * Middleware to handle validation errors and return a consistent response format
 */
const handleValidationErrors = (req, res, next) => {
    const errors = (0, express_validator_1.validationResult)(req);
    if (!errors.isEmpty()) {
        const formattedErrors = errors.array().map((err) => ({
            field: err.type === 'field' ? err.path : 'unknown',
            message: err.msg,
            value: err.value,
        }));
        return res.status(400).json({
            error: 'Validation failed',
            details: formattedErrors,
        });
    }
    next();
};
exports.handleValidationErrors = handleValidationErrors;
