"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.predictionRequestSchema = exports.studentRecordSchema = void 0;
const joi_1 = __importDefault(require("joi"));
exports.studentRecordSchema = joi_1.default.object({
    institution_type: joi_1.default.string().valid('Federal', 'State', 'Private').optional(),
    faculty: joi_1.default.string().optional(),
    department: joi_1.default.string().optional(),
    level: joi_1.default.number().integer().min(100).max(500).optional(),
    entry_mode: joi_1.default.string().valid('UTME', 'DirectEntry', 'Transfer').optional(),
    age: joi_1.default.number().integer().min(15).max(65).optional(),
    sex: joi_1.default.string().valid('Male', 'Female').optional(),
    state_of_origin: joi_1.default.string().optional(),
    residency_status: joi_1.default.string().valid('OnCampus', 'OffCampus').optional(),
    socioeconomic_band: joi_1.default.string().valid('Low', 'Middle', 'High').optional(),
    utme_score: joi_1.default.number().integer().min(0).max(400).optional(),
    post_utme_score: joi_1.default.number().min(0).max(100).optional(),
    entry_qualification: joi_1.default.string().valid('SSCE', 'ND', 'HND', 'Alevel').optional(),
    prev_semester_gpa: joi_1.default.number().min(0).max(5).optional(),
    cumulative_cgpa: joi_1.default.number().min(0).max(5).optional(),
    carryover_courses_count: joi_1.default.number().integer().min(0).optional(),
    failed_courses_prev_semester: joi_1.default.number().integer().min(0).optional(),
    core_courses_failed_total: joi_1.default.number().integer().min(0).optional(),
    course_load_units: joi_1.default.number().integer().min(0).optional(),
    continuous_assessment_avg: joi_1.default.number().min(0).max(40).optional(),
    attendance_rate: joi_1.default.number().min(0).max(1).optional(),
    library_visits_per_month: joi_1.default.number().integer().min(0).optional(),
    lms_logins_per_week: joi_1.default.number().integer().min(0).optional(),
    assignment_submission_rate: joi_1.default.number().min(0).max(1).optional(),
    late_registration_flag: joi_1.default.number().integer().valid(0, 1).optional(),
    financial_clearance_delay_days: joi_1.default.number().integer().min(0).optional(),
    disciplinary_case_flag: joi_1.default.number().integer().valid(0, 1).optional(),
    counselling_visits_semester: joi_1.default.number().integer().min(0).optional(),
    medical_leave_flag: joi_1.default.number().integer().valid(0, 1).optional(),
});
exports.predictionRequestSchema = joi_1.default.object({
    student: exports.studentRecordSchema.required(),
});
