import functions_framework
from google.cloud import bigquery
from datetime import datetime
import uuid

@functions_framework.http
def monthly_grokipedia(request):
    """
    Inserts 10 Grokipedia cement knowledge chunks into BigQuery
    Uses UUID to prevent duplicates across monthly runs
    Triggered via HTTP (curl or Cloud Scheduler)
    """
    client = bigquery.Client(project='cementai-optimiser')
    
    # Generate unique batch ID for this run
    batch_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    # Use MERGE to prevent duplicates (upsert logic)
    sql = f"""
    MERGE `cementai-optimiser.cement_plant.grokipedia_rag` AS target
    USING (
      SELECT * FROM UNNEST([
        STRUCT(
          'chunk_001' AS chunk_id,
          'Energy_reduction' AS topic,
          'Energy Reduction Strategies' AS title,
          'Modern dry-process cement kilns with multi-stage cyclone preheaters reduce thermal energy consumption to 3,100-3,500 MJ per tonne of clinker through optimized heat recovery that preheats raw meal to 800–900°C. Grate coolers recover 20-25% of total process heat by quenching hot clinker and supplying preheated secondary air for combustion.' AS content,
          'https://grokipedia.com/page/Cement_kiln#Energy_Efficiency' AS url,
          120 AS word_count,
          '{batch_id}' AS batch_id,
          TIMESTAMP('{timestamp}') AS last_updated
        ),
        STRUCT(
          'chunk_002',
          'CO2_emissions',
          'CO₂ Emissions Reduction',
          'The cement industry contributes 6-8% of global anthropogenic CO₂ emissions, totaling approximately 2.3 billion metric tons annually. Process emissions from limestone calcination account for 60-70% while fuel combustion contributes the balance. Alternative fuels can achieve thermal substitution rates up to 85% in advanced burners.',
          'https://grokipedia.com/page/Cement_kiln#Environmental_Impacts',
          130,
          '{batch_id}',
          TIMESTAMP('{timestamp}')
        ),
        STRUCT(
          'chunk_003',
          'Kiln_optimization',
          'Cement Kiln Temperature Control',
          'A cement kiln operates at peak temperatures exceeding 1,450°C where raw materials undergo calcination and clinkering reactions. The burning zone requires precise temperature control within ±10°C to prevent ring formations and maintain clinker quality. Kiln efficiency depends on temperature uniformity, residence time, and material feed consistency.',
          'https://grokipedia.com/page/Cement_kiln#Core_Components',
          150,
          '{batch_id}',
          TIMESTAMP('{timestamp}')
        ),
        STRUCT(
          'chunk_004',
          'Quality_control',
          'Quality Consistency Management',
          'Cement quality depends on chemical composition (LSF 90-100, SM 2.0-3.0) and physical properties (Blaine fineness 3200-3800 cm²/g). Real-time monitoring of raw feed variability enables proactive adjustments to grinding and blending. Predictive models can reduce quality variability by 20-30% through early detection of chemistry drift.',
          'https://grokipedia.com/page/Cement_kiln#Quality_Assurance',
          140,
          '{batch_id}',
          TIMESTAMP('{timestamp}')
        ),
        STRUCT(
          'chunk_005',
          'Alternative_fuels',
          'Alternative Fuel Integration',
          'Alternative fuels in cement kilns include refuse-derived fuel (RDF), shredded tires, biomass, and industrial waste. Thermal substitution rates in Europe average 53% with some facilities achieving 85%. High combustion temperatures enable complete destruction of organic contaminants. Challenges include flame stability and alkali buildup.',
          'https://grokipedia.com/page/Cement_kiln#Alternative_Fuels',
          145,
          '{batch_id}',
          TIMESTAMP('{timestamp}')
        ),
        STRUCT(
          'chunk_006',
          'Preheaters',
          'Preheater Efficiency Optimization',
          'Suspension preheaters with 4-6 cyclone stages achieve 80%+ heat recovery efficiency by preheating raw meal in countercurrent gas flow. Each stage facilitates gas-solid separation via centrifugal force. Precalciners enable 85-95% calcination before kiln entry, reducing thermal load and enabling compact kiln designs with capacities exceeding 5,000 tpd.',
          'https://grokipedia.com/page/Cement_kiln#Preheaters_Precalciners',
          135,
          '{batch_id}',
          TIMESTAMP('{timestamp}')
        ),
        STRUCT(
          'chunk_007',
          'Dust_control',
          'Dust and PM Emission Control',
          'Bag filters and electrostatic precipitators achieve PM emission levels below 20 mg/Nm³ through >99% capture efficiency. Differential pressure across bag filters indicates cleaning cycle needs. Stack temperature monitoring helps optimize ID fan power consumption. Reverse-cycle timing affects both PM control and energy efficiency.',
          'https://grokipedia.com/page/Cement_kiln#Environmental_Controls',
          125,
          '{batch_id}',
          TIMESTAMP('{timestamp}')
        ),
        STRUCT(
          'chunk_008',
          'Heat_recovery',
          'Waste Heat Recovery Systems',
          'Waste heat from preheater exhaust and clinker coolers represents 30-40% of total thermal input. Organic Rankine Cycle systems can generate 20-35 kWh per ton of clinker, offsetting 25-30% of plant electricity demand. Payback periods range from 2-4 years in facilities processing over 1 Mt/year.',
          'https://grokipedia.com/page/Cement_kiln#Heat_Recovery',
          128,
          '{batch_id}',
          TIMESTAMP('{timestamp}')
        ),
        STRUCT(
          'chunk_009',
          'Mill_optimization',
          'Grinding Circuit Optimization',
          'Cement grinding accounts for 30-40% of total plant electrical energy. Optimal mill load balancing and separator speed control can reduce specific energy consumption by 5-10%. Ball mill efficiency depends on fill level, liner condition, and particle size distribution. High-efficiency separators improve fineness control.',
          'https://grokipedia.com/page/Cement_kiln#Grinding_Systems',
          132,
          '{batch_id}',
          TIMESTAMP('{timestamp}')
        ),
        STRUCT(
          'chunk_010',
          'Digital_twin',
          'AI and Digital Twin Applications',
          'Digital twins integrate IoT sensor data with physics-based models to enable real-time process optimization. Machine learning models predict clinker quality metrics with >85% accuracy. Reinforcement learning optimizes fuel-air ratios, achieving 3-5% energy reductions. Vision AI enables non-contact temperature profiling with ±10°C precision.',
          'https://grokipedia.com/page/Cement_kiln#Digitalization',
          142,
          '{batch_id}',
          TIMESTAMP('{timestamp}')
        )
      ])
    ) AS source
    ON target.chunk_id = source.chunk_id
    WHEN MATCHED THEN
      UPDATE SET
        topic = source.topic,
        title = source.title,
        content = source.content,
        url = source.url,
        word_count = source.word_count,
        batch_id = source.batch_id,
        last_updated = source.last_updated
    WHEN NOT MATCHED THEN
      INSERT (chunk_id, topic, title, content, url, word_count, batch_id, last_updated)
      VALUES (chunk_id, topic, title, content, url, word_count, batch_id, last_updated)
    """
    
    try:
        job = client.query(sql)
        result = job.result()
        
        # Get stats from MERGE operation
        rows_affected = job.num_dml_affected_rows
        
        return {
            'status': 'SUCCESS',
            'batch_id': batch_id,
            'rows_affected': rows_affected,
            'timestamp': timestamp,
            'message': f'✅ Upserted {rows_affected} Grokipedia chunks (batch: {batch_id[:8]}...)'
        }, 200
        
    except Exception as e:
        return {
            'status': 'ERROR',
            'error': str(e),
            'timestamp': timestamp
        }, 500