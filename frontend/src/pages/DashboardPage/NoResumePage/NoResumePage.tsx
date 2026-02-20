import styles from './NoResumePage.module.scss'
import { Upload } from 'lucide-react'
import { useState, useRef, useEffect } from 'react'

interface Props {
    onConfirm: () => void
}

const NoResumePage = ({ onConfirm }: Props) => {
    const [file, setFile] = useState<File | null>(null)
    const [url, setUrl] = useState<string | null>(null)
    const inputRef = useRef<HTMLInputElement>(null)

    const statsInfo = [
        { metric: "AI-Powered", description: "Start matching" },
        { metric: "1000+", description: "Active Jobs" },
        { metric: "95%", description: "Match Accuracy" },
    ];

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selected = e.target.files?.[0]
        if (!selected) return
        setFile(selected)
        setUrl(URL.createObjectURL(selected))
    }

    useEffect(() => {
        return () => {
            if (url) URL.revokeObjectURL(url)
        }
    }, [url])

    return (
        <div className={styles.wrapper}>
            <div className={styles.content}>
                {!file && (
                    <>
                        <div className={styles.uploadContainer}>
                            <Upload size={40}/>
                        </div>

                        <p className={styles.title}>
                            Let's Find Your Perfect Job Match
                        </p>

                        <p className={styles.text}>
                            Upload your resume to unlock AI-powered job recommendations tailored specifically to your skills, experience, and career goals. Our intelligent matching system analyzes thousands of opportunities to find the best fits for you.
                        </p>

                        <button
                            className={styles.uploadLogoBtn}
                            onClick={() => inputRef.current?.click()}
                        >
                            <Upload size={24}/>
                            Upload Your Resume
                        </button>

                        <div className={styles.stats}>
                            {statsInfo.map(stat => (
                                <div key={stat.metric} className={styles.stat}>
                                    <p className={styles.metric}>{stat.metric}</p>
                                    <p className={styles.description}>{stat.description}</p>
                                </div>
                            ))}
                        </div>
                    </>
                )}

                {file && url && (
                    <div className={styles.previewWrapper}>
                        <div className={styles.resumeCard}>
                            <div className={styles.resumeViewer}>
                                <iframe src={url} title="Resume Preview"/>
                            </div>
                        </div>

                        <div className={styles.actionButtons}>
                            <button
                                className={styles.uploadLogoBtn}
                                onClick={() => inputRef.current?.click()}
                            >
                                Replace Resume
                            </button>

                            <button
                                className={styles.confirmBtn}
                                onClick={onConfirm}
                            >
                                Confirm & Proceed
                            </button>
                        </div>
                    </div>
                )}

                <input
                    ref={inputRef}
                    type="file"
                    hidden
                    accept=".pdf"
                    onChange={handleChange}
                />
            </div>
        </div>
    )
}

export default NoResumePage
