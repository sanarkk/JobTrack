import { useEffect, useState } from "react";
import axios from "axios";
import styles from "./SavedJobsPage.module.scss";
import MatchedJobCard from "../DashboardPage/MatchedJobCard/MatchedJobCard";
import MatchedJobPopup from "../DashboardPage/MatchedJobPopup/MatchedJobPopup";

interface SavedJob {
    saved_id: string;
    job_id: string;
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
    source_file: string | null;
    hash: string;
}

const SavedJobsPage = () => {
    const [savedJobs, setSavedJobs] = useState<SavedJob[]>([]);
    const [selectedJob, setSelectedJob] = useState<SavedJob | null>(null);

    useEffect(() => {
        const fetchSavedJobs = async () => {
            try {
                const res = await axios.get("http://localhost:8001/get_all_saved_jobs/", {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("access_token") || ""}`,
                    },
                });
                setSavedJobs(res.data);
            } catch (error) {
                console.error("Failed to fetch saved jobs:", error);
            }
        };

        fetchSavedJobs();
    }, []);

    const handleDelete = async (jobId: string) => {
        const isConfirmed = confirm("Are you sure you want to delete this job from your saves?");
        if(isConfirmed) {
            try {
                await axios.delete(`http://localhost:8001/delete/${jobId}`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("access_token") || ""}`,
                    },
                });

                setSavedJobs((prev) => prev.filter((job) => job.job_id !== jobId));
                setSelectedJob(null);
            } catch (error) {
                console.error("Failed to delete job:", error);
            }
        }
    };

    return (
        <div className={styles.wrapper}>
            <div className={styles.content}>
                <div className={styles.header}>
                    <h2 className={styles.title}>Saved Jobs</h2>
                    <p className={styles.subTitle}>
                        Positions you've bookmarked for later
                    </p>
                </div>

                {savedJobs.length === 0 ? (
                    <div className={styles.emptyState}>No saved jobs yet.</div>
                ) : (
                    <div className={styles.jobs}>
                        {savedJobs.map((job, index) => (
                            <MatchedJobCard
                                key={job.job_id}
                                job={job}
                                index={index}
                                isSaved={true}
                                variant="saved"
                                onSaveSuccess={() => {}}
                                onViewDetails={() => setSelectedJob(job)}
                                onDelete={() => handleDelete(job.job_id)}
                            >
                                <button
                                    className={styles.deleteBtn}
                                    onClick={() => handleDelete(job.job_id)}
                                >
                                    Delete
                                </button>
                            </MatchedJobCard>
                        ))}
                    </div>
                )}
            </div>

            {selectedJob && (
                <MatchedJobPopup
                    job={selectedJob}
                    variant="saved"
                    isSaved={true}
                    onDelete={() => handleDelete(selectedJob.job_id)}
                    onClose={() => setSelectedJob(null)}
                />
            )}
        </div>
    );
};

export default SavedJobsPage;
