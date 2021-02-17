cube(`Mention`, {
  sql: `SELECT * FROM public.mention`,
  
  joins: {
    Stock: {
      sql: `${CUBE}.stock_id = ${Stock}.id`,
      relationship: `belongsTo`
    }
  },
  
  measures: {
    count: {
      type: `count`,
      drillMembers: [id]
    },

    score: {
      sql: `score`,
      type: `sum`,
      drillMembers: [id, source]
    },

    num_comments: {
      sql: `num_comments`,
      type: `sum`,
    }
  },
  
  dimensions: {
    id: {
      sql: `${CUBE}.stock_id || '-' || ${CUBE}.dt || '-' || ${CUBE}.message`,
      type: `string`,
      primaryKey: true
    },

    message: {
      sql: `message`,
      type: `string`
    },
    
    url: {
      sql: `url`,
      type: `string`
    },
    
    source: {
      sql: `source`,
      type: `string`
    },
    
    dt: {
      sql: `dt`,
      type: `time`
    }
  },
  
  dataSource: `default`
});
