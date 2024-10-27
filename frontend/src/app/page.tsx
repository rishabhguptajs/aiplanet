"use client"

import Image from "next/image";
import { useState, useEffect, useRef } from "react";
import { FiUpload } from "react-icons/fi";
import { RiRobot2Line } from "react-icons/ri";
import { IoSend } from "react-icons/io5";
import { motion, AnimatePresence } from "framer-motion";
import toast, { Toaster } from 'react-hot-toast';

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [messages, setMessages] = useState<Array<{type: 'user' | 'bot', content: string}>>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [pdfId, setPdfId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      
      const formData = new FormData();
      formData.append('file', file);

      toast.promise(
        fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/upload-pdf/`, {
          method: 'POST',
          body: formData,
        }).then(async (response) => {
          if (!response.ok) {
            throw new Error('Failed to upload PDF');
          }

          const data = await response.json();
          setPdfId(data.id);
          setMessages(prev => [...prev, {
            type: 'bot',
            content: `PDF "${file.name}" uploaded successfully! You can now ask questions about it.`
          }]);
          return `PDF "${file.name}" uploaded successfully!`;
        }),
        {
          success: (msg) => msg,
          error: (err) => {
            console.error('Error uploading file:', err);
            setMessages(prev => [...prev, {
              type: 'bot',
              content: 'Sorry, there was an error uploading the PDF. Please try again.'
            }]);
            return 'Error uploading PDF. Please try again.';
          },
          loading: 'Uploading PDF...',
        }
      );
    } else {
      setMessages(prev => [...prev, {
        type: 'bot',
        content: 'Please upload a valid PDF file.'
      }]);
      toast.error('Please upload a valid PDF file.');
    }
  };

  const handleSendMessage = async () => {
    if (inputMessage.trim()) {
        const userMessage = inputMessage.trim();
        setMessages(prev => [...prev, { type: 'user', content: userMessage }]);
        setInputMessage('');

        if (!pdfId) {
            setMessages(prev => [...prev, {
                type: 'bot',
                content: 'Please upload a PDF first before asking questions.'
            }]);
            toast.error('Please upload a PDF first before asking questions.');
            return;
        }

        toast.promise(
          fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/ask-question/${pdfId}`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ question: userMessage }),
          }).then(async (response) => {
              if (!response.ok) {
                  throw new Error('Failed to get answer');
              }

              const data = await response.json();
              setMessages(prev => [...prev, {
                  type: 'bot',
                  content: `${data.answer}`
              }]);
              return 'Answer received!';
          }),
          {
              success: (msg) => msg,
              error: (err) => {
                  console.error('Error getting answer:', err);
                  setMessages(prev => [...prev, {
                      type: 'bot',
                      content: 'Sorry, I encountered an error while processing your question. Please try again.'
                  }]);
                  return 'Error processing your question. Please try again.';
              },
              loading: 'Processing your question...',
          }
        );
    }
};

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <Toaster reverseOrder={false} />
      <motion.div 
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="flex justify-between items-center p-4 border-b backdrop-blur-sm bg-white/70"
      >
        <div className="flex items-center gap-2">
          <motion.div
            whileHover={{ rotate: 360 }}
            transition={{ duration: 0.5 }}
          >
            <RiRobot2Line className="text-2xl sm:text-3xl text-indigo-600" />
          </motion.div>
          <span className="text-lg sm:text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 text-transparent bg-clip-text">AI Planet</span>
        </div>
        <div className="flex items-center gap-2 sm:gap-4">
          {selectedFile && (
            <motion.span 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="hidden sm:inline-block text-sm text-gray-600 truncate max-w-[150px]"
            >
              {selectedFile.name}
            </motion.span>
          )}
          <label className="flex items-center gap-2 cursor-pointer px-3 sm:px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-lg hover:from-indigo-600 hover:to-purple-600 transition-all duration-300 shadow-lg hover:shadow-xl">
            <FiUpload className="text-lg sm:text-base" />
            <span className="hidden sm:inline">Upload PDF</span>
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>
        </div>
      </motion.div>

      <div className="flex-1 overflow-y-auto p-2 sm:p-4 space-y-3 sm:space-y-4">
        {pdfId === null ? (
          <div className="flex items-center justify-center h-full">
            <p className="text-lg text-gray-600">Please upload a PDF to start chatting.</p>
          </div>
        ) : (
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className={`flex ${
                  message.type === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[95%] sm:max-w-[70%] p-3 sm:p-4 rounded-xl sm:rounded-2xl shadow-md ${
                    message.type === 'user'
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white'
                      : 'bg-white text-gray-800'
                  } transform hover:scale-[1.02] transition-transform duration-200 text-sm sm:text-base`}
                >
                  {message.content}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        )}
        <div ref={messagesEndRef} />
      </div>

      <motion.div 
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="border-t p-3 sm:p-4 backdrop-blur-sm bg-white/70"
      >
        <div className="flex gap-2 sm:gap-4 max-w-4xl mx-auto">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Message..."
            className="flex-1 p-2 sm:p-3 border rounded-xl text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm hover:shadow-md transition-shadow duration-200"
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSendMessage}
            disabled={pdfId === null}
            className={`p-2 sm:p-3 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-xl hover:from-indigo-600 hover:to-purple-600 shadow-lg hover:shadow-xl transition-all duration-300 ${pdfId === null ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <IoSend className="text-lg sm:text-xl" />
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}