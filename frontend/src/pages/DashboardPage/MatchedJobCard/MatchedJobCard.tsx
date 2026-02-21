import { useState, useEffect } from "react";
import axios from "axios";
import styles from "./MatchedJobCard.module.scss";
import { MapPin } from "lucide-react";

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
    isSaved: boolean;
    variant: "dashboard" | "saved";
    onViewDetails?: () => void;
    onSaveSuccess: (jobId: string) => void;
    onDelete?: () => void;
}

const MatchedJobCard = ({
                            job,
                            isSaved,
                            variant,
                            onViewDetails,
                            onSaveSuccess,
                            onDelete,
                        }: MatchedJobCardProps) => {
    const [saving, setSaving] = useState(false);
    const [saved, setSaved] = useState(isSaved);

    useEffect(() => {
        setSaved(isSaved);
    }, [isSaved]);

    const hasSalary =
        job.yearly_min_compensation > 0 &&
        job.yearly_max_compensation > 0;

    const addToSaved = async () => {
        if (saving || saved || isSaved) return;

        setSaving(true);

        try {
            await axios.post(
                "http://localhost:8001/save_position",
                null,
                {
                    params: {
                        position_id: job.id,
                    },
                    headers: {
                        Authorization: `Bearer ${
                            localStorage.getItem("access_token") || ""
                        }`,
                        Accept: "application/json",
                    },
                }
            );

            setSaved(true);
            onSaveSuccess(job.id);
        } catch (error) {
            console.error("Error saving job:", error);
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className={styles.job}>
            <div className={styles.mainInfo}>
                <div className={styles.info}>
                    <div className={styles.titleInfo}>
                        <span className={styles.title}>{job.job_title}</span>
                        <span className={styles.matchRate}>95% match</span>
                    </div>

                    <div className={styles.companyInfo}>
            <span className={styles.companyName}>
              {job.company_name}
            </span>

                        <span className={styles.location}>
              <MapPin size={14}/>
                            {job.formatted_workplace_location}
            </span>

                        <span className={styles.onSite}>
              {job.workplace_type}
            </span>
                    </div>
                </div>

                <div className={styles.salarySection}>
                    <p className={styles.salaryText}>Salary range</p>
                    <p className={styles.salary}>
                        {hasSalary
                            ? `$${(
                                (job.yearly_min_compensation +
                                    job.yearly_max_compensation) /
                                2
                            ).toLocaleString()}`
                            : "Not specified"}
                    </p>
                </div>
            </div>

            <div className={styles.body}>
                <p className={styles.description}>
                    {job.requirements_summary}
                </p>

                <div className={styles.skills}>
                    {job.technical_tools.map((skill, i) => (
                        <div className={styles.skill} key={i}>
                            {skill}
                        </div>
                    ))}
                </div>
            </div>

            <div className={styles.btns}>
                <button
                    onClick={onViewDetails}
                    className={styles.detailsBtn}
                >
                    View details
                </button>

                {variant === "dashboard" && (
                    <button
                        onClick={addToSaved}
                        className={styles.saveBtn}
                        disabled={saving || saved}
                    >
                        {saving ? "Saving..." : saved ? "Saved ✓" : "Save"}
                    </button>
                )}

                {variant === "saved" && onDelete && (
                    <button
                        onClick={onDelete}
                        className={styles.deleteBtn}
                    >
                        Delete
                    </button>
                )}
            </div>

        </div>
    );
};

export default MatchedJobCard;
