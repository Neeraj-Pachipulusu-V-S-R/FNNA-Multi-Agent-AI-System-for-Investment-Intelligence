import json
import os
from typing import Dict, Any, List
from core.graph import analyze_news_article
from datetime import datetime

class NewsAnalysisEvaluator:
    """Evaluator for the financial news analysis system"""
    
    def __init__(self, output_dir: str = "evaluation/results"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_test_data(self) -> List[Dict[str, Any]]:
        """Create sample test data for evaluation"""
        test_cases = [
            {
                "article_id": "test_001",
                "headline": "Tesla Reports Record Quarterly Earnings, Beats Analyst Expectations",
                "content": "Tesla Inc. (NASDAQ: TSLA) announced record quarterly earnings of $3.2 billion, significantly beating analyst expectations of $2.8 billion. The electric vehicle maker attributed the strong performance to increased production capacity and growing demand for Model 3 and Model Y vehicles.",
                "published_at": "2024-01-15",
                "expected_sentiment": "positive",
                "expected_impact": "high",
                "expected_risks": ["market"]
            },
            {
                "article_id": "test_002",
                "headline": "Apple Faces Regulatory Challenges in European Union Over App Store Practices",
                "content": "Apple Inc. is facing increased regulatory scrutiny from the European Union regarding its App Store policies. The EU is investigating potential anti-competitive practices and may impose significant fines. This could impact Apple's revenue from its services segment.",
                "published_at": "2024-01-16",
                "expected_sentiment": "negative",
                "expected_impact": "medium",
                "expected_risks": ["regulatory", "financial"]
            },
            {
                "article_id": "test_003",
                "headline": "Microsoft Announces Dividend Increase for Shareholders",
                "content": "Microsoft Corporation announced a 5% increase in its quarterly dividend, reflecting the company's strong cash position and commitment to returning value to shareholders. The tech giant continues to benefit from growing cloud computing revenues.",
                "published_at": "2024-01-17",
                "expected_sentiment": "positive",
                "expected_impact": "low",
                "expected_risks": ["none"]
            }
        ]
        return test_cases
    
    def evaluate_prediction(self, predicted: Dict[str, Any], expected: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate prediction accuracy against expected results
        
        Args:
            predicted: Results from the analysis system
            expected: Expected results for comparison
            
        Returns:
            Evaluation metrics
        """
        metrics = {
            "sentiment_correct": predicted.get("sentiment") == expected.get("expected_sentiment"),
            "impact_correct": predicted.get("impact_level") == expected.get("expected_impact"),
            "risks_overlap": 0.0,
            "overall_accuracy": 0.0
        }
        
        # Calculate risk overlap
        predicted_risks = set(predicted.get("risks", []))
        expected_risks = set(expected.get("expected_risks", []))
        
        if expected_risks and "none" not in expected_risks:
            overlap = len(predicted_risks.intersection(expected_risks))
            metrics["risks_overlap"] = overlap / len(expected_risks)
        elif "none" in expected_risks and "none" in predicted_risks:
            metrics["risks_overlap"] = 1.0
        
        # Calculate overall accuracy
        accuracy_score = sum([
            metrics["sentiment_correct"],
            metrics["impact_correct"],
            metrics["risks_overlap"]
        ]) / 3
        
        metrics["overall_accuracy"] = accuracy_score
        
        return metrics
    
    def run_evaluation(self, test_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run comprehensive evaluation on test data
        
        Args:
            test_data: Optional test data, will create default if not provided
            
        Returns:
            Evaluation results
        """
        if test_data is None:
            test_data = self.create_test_data()
        
        results = []
        total_metrics = {
            "sentiment_accuracy": 0.0,
            "impact_accuracy": 0.0,
            "risk_accuracy": 0.0,
            "overall_accuracy": 0.0
        }
        
        print(f"Running evaluation on {len(test_data)} test cases...")
        
        for i, test_case in enumerate(test_data):
            print(f"\nEvaluating test case {i+1}: {test_case['headline'][:50]}...")
            
            try:
                # Run analysis
                analysis_result = analyze_news_article(test_case)
                final_analysis = analysis_result.get("final_analysis", {})
                
                # Evaluate results
                metrics = self.evaluate_prediction(final_analysis, test_case)
                
                # Store detailed results
                result = {
                    "test_case": test_case,
                    "predicted": final_analysis,
                    "metrics": metrics,
                    "timestamp": datetime.now().isoformat()
                }
                results.append(result)
                
                # Update totals
                total_metrics["sentiment_accuracy"] += metrics["sentiment_correct"]
                total_metrics["impact_accuracy"] += metrics["impact_correct"]
                total_metrics["risk_accuracy"] += metrics["risks_overlap"]
                total_metrics["overall_accuracy"] += metrics["overall_accuracy"]
                
                print(f"  Sentiment: {'✓' if metrics['sentiment_correct'] else '✗'}")
                print(f"  Impact: {'✓' if metrics['impact_correct'] else '✗'}")
                print(f"  Risk Overlap: {metrics['risks_overlap']:.2f}")
                print(f"  Overall: {metrics['overall_accuracy']:.2f}")
                
            except Exception as e:
                print(f"  Error: {str(e)}")
                results.append({
                    "test_case": test_case,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        # Calculate final averages
        num_successful = len([r for r in results if "error" not in r])
        if num_successful > 0:
            for metric in total_metrics:
                total_metrics[metric] = total_metrics[metric] / num_successful
        
        evaluation_summary = {
            "total_test_cases": len(test_data),
            "successful_analyses": num_successful,
            "failed_analyses": len(test_data) - num_successful,
            "average_metrics": total_metrics,
            "detailed_results": results,
            "evaluation_timestamp": datetime.now().isoformat()
        }
        
        # Save results
        output_file = os.path.join(self.output_dir, f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(output_file, "w") as f:
            json.dump(evaluation_summary, f, indent=2)
        
        print(f"\nEvaluation complete! Results saved to: {output_file}")
        print(f"Overall Accuracy: {total_metrics['overall_accuracy']:.2f}")
        
        return evaluation_summary

def run_evaluation():
    """Main evaluation function for backward compatibility"""
    evaluator = NewsAnalysisEvaluator()
    return evaluator.run_evaluation()

if __name__ == "__main__":
    run_evaluation() 