/**
 * Universal Wave Engine - JavaScript API Interface
 * High-level API for easy integration in web and Node.js applications
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Import the Wave Engine implementation
const waveEnginePath = path.join(__dirname, '..', 'javascript', 'wave_engine.js');
const { WaveEngine } = await import(`file://${waveEnginePath}`);

/**
 * Result object for wave processing operations
 */
class WaveResult {
    constructor(symbols, activations, processingTime, timestamp, metadata = {}) {
        this.symbols = symbols;
        this.activations = activations;
        this.processingTime = processingTime;
        this.timestamp = timestamp;
        this.metadata = metadata;
    }
}

/**
 * Universal Wave Engine API
 * Provides high-level interface for wave-based cognition
 */
class UniversalWaveAPI {
    constructor(config = {}) {
        this.config = config;
        this.engine = new WaveEngine();
        this.sessionId = `wave_session_${Date.now()}`;
        this.history = [];
    }

    /**
     * Process input through wave interference
     * @param {string|Array<string>} inputData - String or array of strings to process
     * @param {boolean} returnMetadata - Whether to include processing metadata
     * @returns {WaveResult} Result object with activations and metadata
     */
    process(inputData, returnMetadata = true) {
        const startTime = performance.now();
        
        // Convert single string to array
        const symbols = Array.isArray(inputData) ? inputData : [inputData];
        
        // Process through wave engine
        const activations = this.engine.process(symbols);
        
        const processingTime = (performance.now() - startTime) / 1000; // Convert to seconds
        
        const result = new WaveResult(
            symbols,
            activations,
            processingTime,
            Date.now(),
            returnMetadata ? {
                sessionId: this.sessionId,
                engineVersion: '1.0.0',
                algorithm: 'wave_interference',
                performanceClass: processingTime < 0.001 ? 'sub_millisecond' : 'fast'
            } : {}
        );
        
        // Store in history
        this.history.push(result);
        
        return result;
    }

    /**
     * Perform reasoning using wave interference
     * @param {Array<string>} context - Array of context symbols
     * @param {string} query - Query symbol to reason about
     * @returns {Object} Dictionary of reasoning results
     */
    reason(context, query) {
        // Combine context and query
        const allSymbols = [...context, query];
        const result = this.process(allSymbols);
        
        // Extract query activation relative to context
        const queryActivation = result.activations[query] || 0.0;
        const contextActivations = {};
        
        context.forEach(symbol => {
            if (result.activations[symbol] !== undefined) {
                contextActivations[symbol] = result.activations[symbol];
            }
        });
        
        return {
            query: query,
            queryActivation: queryActivation,
            contextActivations: contextActivations,
            reasoningConfidence: Math.abs(queryActivation),
            processingTime: result.processingTime
        };
    }

    /**
     * Detect contradictions using wave cancellation
     * @param {Array<string>} statements - Array of statements to check for contradictions
     * @returns {Object} Dictionary with contradiction analysis
     */
    detectContradictions(statements) {
        const result = this.process(statements);
        
        // Find opposing activations (likely contradictions)
        const activations = Object.values(result.activations);
        const positive = activations.filter(a => a > 0);
        const negative = activations.filter(a => a < 0);
        
        let contradictionScore = 0.0;
        if (positive.length > 0 && negative.length > 0) {
            const maxPositive = Math.max(...positive);
            const minNegative = Math.min(...negative);
            contradictionScore = Math.abs(maxPositive - minNegative);
        }
        
        return {
            contradictionDetected: contradictionScore > 0.5,
            contradictionScore: contradictionScore,
            statementActivations: result.activations,
            positiveStatements: statements.filter(stmt => result.activations[stmt] > 0),
            negativeStatements: statements.filter(stmt => result.activations[stmt] < 0),
            processingTime: result.processingTime
        };
    }

    /**
     * Predict patterns using wave propagation
     * @param {Array<string>} sequence - Input sequence
     * @param {number} predictNext - Number of next items to predict
     * @returns {Object} Dictionary with pattern predictions
     */
    predictPatterns(sequence, predictNext = 1) {
        // Process sequence to get wave state
        const result = this.process(sequence);
        
        // Use wave phases to predict temporal continuation
        const predictions = [];
        for (let i = 0; i < predictNext; i++) {
            // Simulate temporal evolution
            const nextTime = result.timestamp + (i + 1) * 0.1;
            const predictedActivation = this.engine.getActivation(`predicted_${i}`, nextTime);
            predictions.push({
                predictionId: i,
                predictedActivation: predictedActivation,
                confidence: Math.abs(predictedActivation)
            });
        }
        
        return {
            sequence: sequence,
            predictions: predictions,
            sequenceActivations: result.activations,
            processingTime: result.processingTime
        };
    }

    /**
     * Process multiple inputs in batch
     * @param {Array<string|Array<string>>} batch - Array of inputs to process
     * @returns {Array<WaveResult>} Array of WaveResult objects
     */
    batchProcess(batch) {
        return batch.map(item => this.process(item));
    }

    /**
     * Export session history
     * @param {string} format - Export format ('json')
     * @returns {string} Serialized session data
     */
    exportSession(format = 'json') {
        if (format === 'json') {
            const sessionData = {
                sessionId: this.sessionId,
                totalOperations: this.history.length,
                history: this.history.map(result => ({
                    symbols: result.symbols,
                    activations: result.activations,
                    processingTime: result.processingTime,
                    timestamp: result.timestamp,
                    metadata: result.metadata
                }))
            };
            return JSON.stringify(sessionData, null, 2);
        } else {
            throw new Error(`Unsupported export format: ${format}`);
        }
    }

    /**
     * Get performance statistics for the session
     * @returns {Object} Dictionary with performance metrics
     */
    getPerformanceStats() {
        if (this.history.length === 0) {
            return { error: 'No operations performed yet' };
        }
        
        const processingTimes = this.history.map(result => result.processingTime);
        const totalSymbols = this.history.reduce((sum, result) => sum + result.symbols.length, 0);
        const totalTime = processingTimes.reduce((sum, time) => sum + time, 0);
        
        return {
            totalOperations: this.history.length,
            totalSymbolsProcessed: totalSymbols,
            avgProcessingTime: totalTime / this.history.length,
            minProcessingTime: Math.min(...processingTimes),
            maxProcessingTime: Math.max(...processingTimes),
            symbolsPerSecond: totalTime > 0 ? totalSymbols / totalTime : 0,
            sessionDuration: (Date.now() - parseInt(this.sessionId.split('_').pop())) / 1000
        };
    }
}

// Convenience functions for quick access
export function waveProcess(symbols) {
    const api = new UniversalWaveAPI();
    const result = api.process(symbols);
    return result.activations;
}

export function waveReason(context, query) {
    const api = new UniversalWaveAPI();
    return api.reason(context, query);
}

export function waveDetectContradictions(statements) {
    const api = new UniversalWaveAPI();
    const result = api.detectContradictions(statements);
    return result.contradictionDetected;
}

// Export the main class
export { UniversalWaveAPI, WaveResult };

// Main demo function
async function main() {
    console.log("🌊 Universal Wave Engine API Demo");
    console.log("=".repeat(50));
    
    const api = new UniversalWaveAPI();
    
    // Demo 1: Basic processing
    console.log("\n1. Basic Processing:");
    const result = api.process(["thinking", "mind", "consciousness"]);
    console.log(`Symbols: ${JSON.stringify(result.symbols)}`);
    console.log(`Activations: ${JSON.stringify(result.activations)}`);
    console.log(`Processing time: ${result.processingTime.toFixed(6)}s`);
    
    // Demo 2: Reasoning
    console.log("\n2. Reasoning:");
    const reasoning = api.reason(["birds", "fly"], "penguins");
    console.log(`Query: ${reasoning.query}`);
    console.log(`Confidence: ${reasoning.reasoningConfidence.toFixed(3)}`);
    
    // Demo 3: Contradiction detection
    console.log("\n3. Contradiction Detection:");
    const contradictions = api.detectContradictions(["birds", "fly", "penguins", "cannot"]);
    console.log(`Contradiction detected: ${contradictions.contradictionDetected}`);
    console.log(`Score: ${contradictions.contradictionScore.toFixed(3)}`);
    
    // Demo 4: Performance stats
    console.log("\n4. Performance Statistics:");
    const stats = api.getPerformanceStats();
    console.log(`Operations: ${stats.totalOperations}`);
    console.log(`Avg time: ${stats.avgProcessingTime.toFixed(6)}s`);
    console.log(`Symbols/sec: ${Math.round(stats.symbolsPerSecond)}`);
}

// Run demo if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
    main().catch(console.error);
} 