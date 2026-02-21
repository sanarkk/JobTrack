import styles from "./MatchedJobCard.module.scss";
import {MapPin} from "lucide-react"

interface MatchedJob {
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
}

interface MatchedJobCardProps {
    job: MatchedJob;
    index: number;
    onViewDetails?: () => void;
}

const MatchedJobCard = ({job, index, onViewDetails}: MatchedJobCardProps) => {

    const hasSalary =
        job.yearly_min_compensation > 0 &&
        job.yearly_max_compensation > 0;

    return (
        <div className={styles.job} key={index}>
            <div className={styles.mainInfo}>
                <div className={styles.info}>
                    <div className={styles.titleInfo}>
                        <span className={styles.title}>{job.job_title}</span>
                        <span className={styles.matchRate}>95% match</span>
                    </div>
                    <div className={styles.companyInfo}>
                        <span className={styles.companyName}>{job.company_name}</span>
                        <span className={styles.location}><MapPin size={14}/>{job.formatted_workplace_location}</span>
                        <span className={styles.onSite}>{job.workplace_type}</span>
                    </div>
                </div>
                <div className={styles.salarySection}>
                    <p className={styles.salaryText}>Salary range</p>
                    <p className={styles.salary}>{hasSalary
                        ? (job.yearly_min_compensation + job.yearly_max_compensation) / 2 + `$`
                        : "Not specified"}</p>
                </div>
            </div>
            <div className={styles.body}>
                <p className={styles.description}>{job.requirements_summary}</p>
                <div className={styles.skills}>
                    {job.technical_tools.map((skill, index) => (
                        <div className={styles.skill} key={index}>
                            {skill}
                        </div>
                    ))}
                </div>
            </div>
            <div className={styles.btns}>
                <button onClick={onViewDetails} className={styles.detailsBtn}>View details</button>
                <button className={styles.saveBtn}>Save</button>
            </div>
        </div>
    );
};

export default MatchedJobCard;