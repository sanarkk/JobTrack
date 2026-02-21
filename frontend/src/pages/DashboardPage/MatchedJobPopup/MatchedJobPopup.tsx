import styles from "./MatchedJobPopup.module.scss";
import { ArrowLeft, MapPin, TrendingUp, Briefcase,} from "lucide-react";

interface MatchedJobPopupProps {
    job: {
        id: string;
        job_title: string;
        job_category: string;
        seniority_level: string;
        requirements_summary: string;
        technical_tools: string[];
        formatted_workplace_location: string;
        province: string;
        commitment: string;
        workplace_type: string;
        yearly_min_compensation: number;
        yearly_max_compensation: number;
        company_name: string;
        apply_url: string;
        source_file: string;
        hash: string;
    };
    onClose: () => void;
    variant: "dashboard" | "saved";
    isSaved: boolean;
    onSave?: () => void;
    onDelete?: () => void;

}

const MatchedJobPopup = ({
                                   job,
                                   onClose,
                                   variant,
                                   isSaved,
                                   onSave,
                                   onDelete,
                               }: MatchedJobPopupProps) => {

    const hasSalary =
        job.yearly_min_compensation > 0 &&
        job.yearly_max_compensation > 0;
    return (
        <div className={styles.overlay}>
            <div className={styles.container}>
                <button className={styles.backBtn} onClick={onClose}>
                    <ArrowLeft size={20}/>
                    <span>Back to Job Matches</span>
                </button>
                <div className={styles.job} key={job.hash}>
                    <div className={styles.mainInfo}>
                        <div className={styles.info}>
                            <div className={styles.titleInfo}>
                                <span className={styles.title}>{job.job_title}</span>
                            </div>
                            <div className={styles.companyInfo}>
                                <span className={styles.companyName}>{job.company_name}</span>
                                <span className={styles.location}><MapPin size={14}/>{job.formatted_workplace_location}</span>
                                <span className={styles.onSite}>{job.workplace_type}</span>
                            </div>
                            <div style={{display: "flex", gap: 12, alignItems: "center"}}>
                                <span className={styles.matchRate}><TrendingUp size={20}/>95% match</span>
                                <span className={styles.workType}><Briefcase size={20}/>{job.commitment.replace(/[{}"]/g, "")}</span>
                                <span className={styles.workType}>Seniority: {job.seniority_level}</span>
                            </div>
                        </div>
                        <div className={styles.salarySection}>
                            <p className={styles.salaryText}>Salary range</p>
                            <p className={styles.salary}>{hasSalary
                                ? (job.yearly_min_compensation + job.yearly_max_compensation) / 2 + `$`
                                : "Not specified"}</p>
                        </div>
                    </div>
                    <div className={styles.btns}>
                        <a href={job.apply_url} target="_blank" className={styles.detailsBtn}>Apply</a>
                        {variant === "dashboard" && (
                            <button
                                className={styles.saveBtn}
                                onClick={onSave}
                                disabled={isSaved}
                            >
                                {isSaved ? "Saved ✓" : "Save"}
                            </button>
                        )}

                        {variant === "saved" && (
                            <button
                                className={styles.deleteBtn}
                                onClick={onDelete}
                            >
                                Delete
                            </button>
                        )}
                    </div>
                </div>
                <div className={styles.description}>
                    <p className={styles.title}>Description</p>
                    <p className={styles.text}>{job.requirements_summary}</p>
                </div>
                <div className={styles.skillContainer}>
                <p className={styles.title}>Required Skills</p>
                    <div className={styles.skills}>
                        {job.technical_tools.map((skill, index) => (
                            <div className={styles.skill} key={index}>
                                {skill}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MatchedJobPopup;
