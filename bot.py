import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send } from 'lucide-react';

const Dashboard = () => {
  const [botStatus, setBotStatus] = useState('offline');
  const [chatMessages, setChatMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const chatContainerRef = useRef(null);

  const responses = {
    general: {
      what_is_instagram: `Instagram is a social media platform owned by Meta (formerly Facebook) that focuses on photo and video sharing. Key features include:
1. Photo & Video Sharing
2. Stories - 24-hour temporary content
3. Reels - Short-form vertical videos
4. Direct Messages
5. Instagram Shopping
6. Business Tools & Analytics`,
      
      features: `Instagram's Main Features:
1. Feed Posts: Share photos and videos
2. Stories: 24-hour content with filters and stickers
3. Reels: 15-90 second vertical videos
4. IGTV: Longer form vertical video content
5. Direct Messages: Private messaging
6. Explore Page: Discover new content
7. Shopping: Buy products directly
8. Live Streaming: Real-time video broadcasts`,
      
      algorithm: `Instagram's Algorithm Priorities:
1. Interest: Content similar to what users engage with
2. Timeliness: Recent posts get priority
3. Relationship: Content from accounts users interact with
4. Frequency: How often users open Instagram
5. Following: Content from all followed accounts
6. Usage: Time spent on the platform`
    },
    
    content_creation: {
      photo_tips: `Instagram Photo Best Practices:
1. Use high-quality images (1080x1080px minimum)
2. Follow the rule of thirds
3. Maintain consistent lighting
4. Use relevant hashtags (up to 30)
5. Write engaging captions
6. Tag relevant accounts
7. Use location tags for better reach`,
      
      video_tips: `Video Content Guidelines:
1. Keep Reels between 15-30 seconds
2. Use trending music and sounds
3. Start with a hook
4. Add captions for accessibility
5. Use relevant hashtags
6. Post at peak engagement times
7. Create series or themed content`,
      
      story_tips: `Story Creation Tips:
1. Use interactive stickers
2. Add location and hashtag stickers
3. Use polls and questions
4. Share behind-the-scenes content
5. Highlight important stories
6. Use branded colors and fonts
7. Maintain consistent posting schedule`
    },
    
    business: {
      account_setup: `Business Account Setup:
1. Convert to business account
2. Complete profile information
3. Add contact information
4. Set category and business type
5. Connect Facebook page
6. Set up Instagram Shopping
7. Add action buttons`,
      
      marketing: `Marketing Strategies:
1. Content calendar planning
2. Influencer collaborations
3. User-generated content
4. Instagram ads setup
5. Cross-promotion strategies
6. Engagement tactics
7. Analytics monitoring`,
      
      analytics: `Understanding Instagram Analytics:
1. Account reach and impressions
2. Engagement rates
3. Story completion rates
4. Website clicks
5. Profile visits
6. Follower growth
7. Best posting times`
    }
  };

  const generateBotResponse = (message) => {
    if (!message) return "Hello! I'm your Instagram assistant. Ask me anything about Instagram - from basic features to advanced marketing strategies!";
    
    const keywords = message.toLowerCase().split(' ');
    let bestResponse = "";

    const keywordMap = {
      general: {
        what_is: ['what', 'instagram', 'platform', 'about'],
        features: ['features', 'options', 'tools', 'capabilities'],
        algorithm: ['algorithm', 'feed', 'reach', 'visibility']
      },
      content_creation: {
        photo: ['photo', 'picture', 'image', 'photography', 'camera'],
        video: ['video', 'reel', 'reels', 'film', 'record'],
        story: ['story', 'stories', 'highlight', 'temporary']
      },
      business: {
        setup: ['setup', 'business', 'account', 'profile'],
        marketing: ['marketing', 'promote', 'advertise', 'campaign'],
        analytics: ['analytics', 'insights', 'statistics', 'performance']
      }
    };

    // Check for general "what is" questions first
    if (keywords.includes('what') && keywords.includes('instagram')) {
      return responses.general.what_is_instagram;
    }

    for (const [category, subcategories] of Object.entries(keywordMap)) {
      for (const [subcat, words] of Object.entries(subcategories)) {
        if (keywords.some(keyword => words.includes(keyword))) {
          bestResponse = responses[category][`${subcat}_${category === 'general' ? subcat : 'tips'}`];
          break;
        }
      }
      if (bestResponse) break;
    }

    return bestResponse || "I understand you're asking about Instagram. Could you please be more specific about what you'd like to know? I can help with features, content creation, business strategies, or general information.";
  };

  // Rest of the component remains the same (TypingMessage, scrollToBottom, toggleBotStatus, handleSendMessage)
  const TypingMessage = ({ content = '' }) => {
    const [displayText, setDisplayText] = useState('');
    const [currentIndex, setCurrentIndex] = useState(0);
    const contentRef = useRef(content);

    useEffect(() => {
      contentRef.current = content;
    }, [content]);

    useEffect(() => {
      if (!content) {
        setIsTyping(false);
        return;
      }

      if (currentIndex < content.length) {
        const timeout = setTimeout(() => {
          setDisplayText(prev => prev + content[currentIndex]);
          setCurrentIndex(prev => prev + 1);
          scrollToBottom();
        }, Math.random() * 30 + 20);

        return () => clearTimeout(timeout);
      } else {
        setIsTyping(false);
      }
    }, [currentIndex, content]);

    return <p className="whitespace-pre-line">{displayText}</p>;
  };

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

  const toggleBotStatus = () => {
    setBotStatus(botStatus === 'online' ? 'offline' : 'online');
  };

  const handleSendMessage = () => {
    if (!newMessage.trim() || isTyping) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: newMessage,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setChatMessages(prev => [...prev, userMessage]);
    setNewMessage('');
    setIsTyping(true);

    setTimeout(() => {
      const botResponse = generateBotResponse(newMessage);
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: botResponse,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isTyping: true
      };
      setChatMessages(prev => [...prev, botMessage]);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
            Instagram Assistant
          </h1>
          <div className="flex items-center gap-2">
            <span className={`inline-block w-3 h-3 rounded-full ${
              botStatus === 'online' ? 'bg-green-500' : 'bg-red-500'
            } animate-pulse`}></span>
            <span className="mr-2 font-medium">{botStatus === 'online' ? 'Online' : 'Offline'}</span>
            <Button 
              onClick={toggleBotStatus}
              variant={botStatus === 'online' ? 'destructive' : 'default'}
              className="shadow-lg hover:shadow-xl transition-all"
            >
              {botStatus === 'online' ? 'Stop Assistant' : 'Start Assistant'}
            </Button>
          </div>
        </div>

        <Card className="h-[600px] flex flex-col bg-white/50 backdrop-blur-lg border border-purple-100">
          <CardHeader>
            <CardTitle className="text-purple-900">Ask me anything about Instagram!</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 flex flex-col">
            <div ref={chatContainerRef} className="flex-1 overflow-y-auto mb-4 space-y-4">
              {chatMessages.map(message => (
                <div
                  key={message.id}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[70%] p-3 rounded-lg ${
                      message.type === 'user'
                        ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white'
                        : 'bg-white'
                    }`}
                  >
                    {message.type === 'bot' && message.isTyping ? (
                      <TypingMessage content={message.content} />
                    ) : (
                      <p className="whitespace-pre-line">{message.content}</p>
                    )}
                    <span className="text-xs mt-1 block opacity-70">
                      {message.timestamp}
                    </span>
                  </div>
                </div>
              ))}
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-white p-3 rounded-lg">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]" />
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]" />
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div className="flex gap-2">
              <Input
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Ask anything about Instagram..."
                className="flex-1 bg-white/70 border-purple-100"
                disabled={isTyping}
              />
              <Button 
                onClick={handleSendMessage}
                className="bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white"
                disabled={isTyping}
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
