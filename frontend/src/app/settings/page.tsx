"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import { Save } from "lucide-react";

export default function SettingsPage() {
  const [model, setModel] = useState("openai/gpt-4o-mini");
  const [temperature, setTemperature] = useState("0.7");
  const [maxTokens, setMaxTokens] = useState("1000");

  useEffect(() => {
    // Load saved settings if they exist
    const savedModel = localStorage.getItem("ai_model");
    const savedTemp = localStorage.getItem("ai_temperature");
    const savedTokens = localStorage.getItem("ai_max_tokens");

    if (savedModel) setModel(savedModel);
    if (savedTemp) setTemperature(savedTemp);
    if (savedTokens) setMaxTokens(savedTokens);
  }, []);

  const handleSave = () => {
    localStorage.setItem("ai_model", model);
    localStorage.setItem("ai_temperature", temperature);
    localStorage.setItem("ai_max_tokens", maxTokens);
    
    // In a real scenario, this might also trigger an API call to save settings to the backend
    toast.success("AI Configuration saved successfully!");
  };

  return (
    <div className="space-y-6 max-w-3xl">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>AI Configuration</CardTitle>
          <CardDescription>
            Configure OpenRouter model parameters used for Lead Qualification.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="model">OpenRouter Model</Label>
            <Select value={model} onValueChange={(val) => val && setModel(val)}>
              <SelectTrigger id="model">
                <SelectValue placeholder="Select a model" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="openai/gpt-4o-mini">OpenAI: GPT-4o Mini</SelectItem>
                <SelectItem value="openai/gpt-4o">OpenAI: GPT-4o</SelectItem>
                <SelectItem value="anthropic/claude-3.5-sonnet">Anthropic: Claude 3.5 Sonnet</SelectItem>
                <SelectItem value="meta-llama/llama-3-70b-instruct">Meta: Llama 3 70B</SelectItem>
              </SelectContent>
            </Select>
            <p className="text-[0.8rem] text-muted-foreground">The AI model to use for generating qualification responses.</p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="temperature">Temperature</Label>
            <Input 
              id="temperature" 
              type="number" 
              step="0.1" 
              min="0" 
              max="2" 
              value={temperature}
              onChange={(e) => setTemperature(e.target.value)}
            />
            <p className="text-[0.8rem] text-muted-foreground">Controls randomness. Lower values are more deterministic (0-2).</p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="maxTokens">Max Tokens</Label>
            <Input 
              id="maxTokens" 
              type="number" 
              step="100" 
              min="100" 
              value={maxTokens}
              onChange={(e) => setMaxTokens(e.target.value)}
            />
            <p className="text-[0.8rem] text-muted-foreground">The maximum number of tokens to generate in the response.</p>
          </div>

          <Button onClick={handleSave} className="w-full sm:w-auto">
            <Save className="mr-2 h-4 w-4" /> Save Configuration
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
