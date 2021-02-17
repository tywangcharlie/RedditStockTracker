cube(`Stock`, {
  sql: `SELECT * FROM public.stock`,
  
  joins: {
    
  },
  
  measures: {
    count: {
      type: `count`,
      drillMembers: [id, symbol, name]
    }
  },
  
  dimensions: {
    id: {
      sql: `id`,
      type: `number`,
      primaryKey: true
    },
    
    isEtf: {
      sql: `is_etf`,
      type: `string`
    },
    
    symbol: {
      sql: `symbol`,
      type: `string`
    },
    
    exchange: {
      sql: `exchange`,
      type: `string`
    },
    
    name: {
      sql: `name`,
      type: `string`
    }
  },
  
  dataSource: `default`
});
