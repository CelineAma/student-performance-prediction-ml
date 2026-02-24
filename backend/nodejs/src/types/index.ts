import { Request } from 'express';

export interface AuthenticatedRequest extends Request {
  user?: { username: string };
}

export interface StudentRecord {
  institution_type?: string;
  faculty?: string;
  department?: string;
  level?: number;
  entry_mode?: string;
  age?: number;
  sex?: string;
  state_of_origin?: string;
  residency_status?: string;
  socioeconomic_band?: string;
  utme_score?: number;
  post_utme_score?: number;
  entry_qualification?: string;
  prev_semester_gpa?: number;
  cumulative_cgpa?: number;
  carryover_courses_count?: number;
  failed_courses_prev_semester?: number;
  core_courses_failed_total?: number;
  course_load_units?: number;
  continuous_assessment_avg?: number;
  attendance_rate?: number;
  library_visits_per_month?: number;
  lms_logins_per_week?: number;
  assignment_submission_rate?: number;
  late_registration_flag?: number;
  financial_clearance_delay_days?: number;
  disciplinary_case_flag?: number;
  counselling_visits_semester?: number;
  medical_leave_flag?: number;
}

export interface PredictionRequest {
  student: StudentRecord;
}

export interface PredictionResponse {
  prediction: 0 | 1; // 0 = not at risk, 1 = at risk
  probability?: number; // optional risk probability if provided by ML service
  explanation_url?: string; // optional URL to SHAP explanation if available
}

export interface AuthRequest {
  username: string;
  password: string;
}

export interface AuthResponse {
  token: string;
}
