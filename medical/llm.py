from typing import List, Tuple
import re


def summarize_transcript(transcript_chunk: str, length: int = 8, tone: str = "neutral") -> Tuple[List[str], List[str]]:
    """
    Simple rule-based summarization for demo purposes.
    Extracts key points and action items from meeting transcripts.
    """
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', transcript_chunk)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Keywords for identifying important content
    decision_keywords = ['decided', 'agreed', 'concluded', 'resolved', 'approved', 'rejected', 'chose', 'selected']
    action_keywords = ['action', 'task', 'todo', 'need to', 'will', 'should', 'must', 'assign', 'responsible', 'deadline', 'due']
    meeting_keywords = ['meeting', 'discuss', 'review', 'present', 'propose', 'suggest', 'recommend', 'plan', 'strategy']
    
    summary_bullets = []
    action_items = []
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        
        # Check for action items
        if any(word in sentence_lower for word in action_keywords):
            if len(action_items) < max(3, length // 2):
                action_items.append(sentence.strip())
        
        # Check for key decisions and important points
        elif any(word in sentence_lower for word in decision_keywords + meeting_keywords):
            if len(summary_bullets) < length:
                summary_bullets.append(sentence.strip())
    
    # Add fallback content if not enough found
    if len(summary_bullets) < 3:
        summary_bullets.extend([
            "Meeting covered important topics and decisions",
            "Team discussed current progress and challenges", 
            "Key points were reviewed and next steps identified"
        ])
    
    if len(action_items) < 2:
        action_items.extend([
            "Follow up on discussed action items",
            "Prepare materials for next meeting"
        ])
    
    return summary_bullets[:length], action_items[:max(3, length // 2)]


