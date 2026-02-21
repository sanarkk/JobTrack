import { useState, useRef, useEffect } from "react";
import { Sparkles, Send } from "lucide-react";
import styles from "./AiAssistantPage.module.scss";

interface Message {
    id: number;
    text: string;
    sender: "user" | "assistant";
    timestamp: Date;
}

const AiAssistantPage = () => {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: 1,
            text: "Hi! I'm your AI Career Assistant. I can help you optimize your resume, identify missing skills, craft compelling summaries, and generate tailored cover letters. How can I assist you today?",
            sender: "assistant",
            timestamp: new Date(),
        },
    ]);

    const [inputValue, setInputValue] = useState("");
    const [loading, setLoading] = useState(false);

    const messagesEndRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, loading]);

    const handleSend = async () => {
        if (!inputValue.trim() || loading) return;

        const userMessage: Message = {
            id: Date.now(),
            text: inputValue.trim(),
            sender: "user",
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setInputValue("");
        setLoading(true);

        try {
            const response = await fetch(
                `http://0.0.0.0:8001/chatbot/send_message_ai/?text=${encodeURIComponent(
                    userMessage.text
                )}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${
                            localStorage.getItem("access_token") || ""
                        }`,
                    },
                }
            );

            const data = await response.json();

            const aiMessage: Message = {
                id: Date.now() + 1,
                text: typeof data === "string" ? data : JSON.stringify(data),
                sender: "assistant",
                timestamp: new Date(),
            };

            setMessages((prev) => [...prev, aiMessage]);
        } catch {
            setMessages((prev) => [
                ...prev,
                {
                    id: Date.now() + 2,
                    text: "⚠️ Something went wrong. Try again.",
                    sender: "assistant",
                    timestamp: new Date(),
                },
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.wrapper}>
            <div className={styles.chat}>
                <div className={styles.header}>
                    <div className={styles.headerLeft}>
                        <div className={styles.iconBox}>
                            <Sparkles size={18} />
                        </div>
                        <div>
                            <h2>AI Career Assistant</h2>
                            <p>Here to help optimize your application</p>
                        </div>
                    </div>
                </div>

                <div className={styles.messages}>
                    {messages.map((message) => (
                        <div
                            key={message.id}
                            className={
                                message.sender === "user"
                                    ? styles.messageRowUser
                                    : styles.messageRowAssistant
                            }
                        >
                            <div
                                className={
                                    message.sender === "user"
                                        ? styles.messageUser
                                        : styles.messageAssistant
                                }
                            >
                                <p>{message.text}</p>
                                <span>
                  {message.timestamp.toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                  })}
                </span>
                            </div>
                        </div>
                    ))}

                    {loading && (
                        <div className={styles.messageRowAssistant}>
                            <div className={styles.messageAssistant}>
                                <p>Typing...</p>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                <div className={styles.inputArea}>
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleSend()}
                        placeholder="Ask me anything about your application..."
                    />
                    <button
                        onClick={handleSend}
                        disabled={!inputValue.trim() || loading}
                        className={styles.sendBtn}
                    >
                        <Send size={16} />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default AiAssistantPage;
