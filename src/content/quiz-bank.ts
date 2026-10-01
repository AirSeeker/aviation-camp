export type ExamQuestion = {
  id: string;
  question: string;
  options: string[];
  correctAnswer: number;
  explanation: string;
  source?: string;
  reference?: { book: string; chapter: string; anchor: string };
};

import content_quizzes_AFH_ch01_json from '../../content/quizzes/AFH/ch01.json';
import content_quizzes_AFH_ch02_json from '../../content/quizzes/AFH/ch02.json';
import content_quizzes_AFH_ch03_json from '../../content/quizzes/AFH/ch03.json';
import content_quizzes_AFH_ch04_json from '../../content/quizzes/AFH/ch04.json';
import content_quizzes_AFH_ch05_json from '../../content/quizzes/AFH/ch05.json';
import content_quizzes_AFH_ch06_json from '../../content/quizzes/AFH/ch06.json';
import content_quizzes_AFH_ch07_json from '../../content/quizzes/AFH/ch07.json';
import content_quizzes_AFH_ch08_json from '../../content/quizzes/AFH/ch08.json';
import content_quizzes_AFH_ch09_json from '../../content/quizzes/AFH/ch09.json';
import content_quizzes_AFH_ch10_json from '../../content/quizzes/AFH/ch10.json';
import content_quizzes_AFH_ch11_json from '../../content/quizzes/AFH/ch11.json';
import content_quizzes_AFH_ch12_json from '../../content/quizzes/AFH/ch12.json';
import content_quizzes_AFH_ch13_json from '../../content/quizzes/AFH/ch13.json';
import content_quizzes_AFH_ch14_json from '../../content/quizzes/AFH/ch14.json';
import content_quizzes_AFH_ch15_json from '../../content/quizzes/AFH/ch15.json';
import content_quizzes_AFH_ch16_json from '../../content/quizzes/AFH/ch16.json';
import content_quizzes_AFH_ch17_json from '../../content/quizzes/AFH/ch17.json';
import content_quizzes_AFH_ch18_json from '../../content/quizzes/AFH/ch18.json';
import content_quizzes_Instrument_ch01_json from '../../content/quizzes/Instrument/ch01.json';
import content_quizzes_Instrument_ch02_json from '../../content/quizzes/Instrument/ch02.json';
import content_quizzes_Instrument_ch03_json from '../../content/quizzes/Instrument/ch03.json';
import content_quizzes_Instrument_ch04_json from '../../content/quizzes/Instrument/ch04.json';
import content_quizzes_Instrument_ch05_json from '../../content/quizzes/Instrument/ch05.json';
import content_quizzes_Instrument_ch06_json from '../../content/quizzes/Instrument/ch06.json';
import content_quizzes_Instrument_ch07_json from '../../content/quizzes/Instrument/ch07.json';
import content_quizzes_Instrument_ch08_json from '../../content/quizzes/Instrument/ch08.json';
import content_quizzes_Instrument_ch09_json from '../../content/quizzes/Instrument/ch09.json';
import content_quizzes_Instrument_ch10_json from '../../content/quizzes/Instrument/ch10.json';
import content_quizzes_Instrument_ch11_json from '../../content/quizzes/Instrument/ch11.json';
import content_quizzes_InstrumentProcedures_ch01_json from '../../content/quizzes/InstrumentProcedures/ch01.json';
import content_quizzes_InstrumentProcedures_ch02_json from '../../content/quizzes/InstrumentProcedures/ch02.json';
import content_quizzes_InstrumentProcedures_ch03_json from '../../content/quizzes/InstrumentProcedures/ch03.json';
import content_quizzes_InstrumentProcedures_ch04_json from '../../content/quizzes/InstrumentProcedures/ch04.json';
import content_quizzes_InstrumentProcedures_ch05_json from '../../content/quizzes/InstrumentProcedures/ch05.json';
import content_quizzes_InstrumentProcedures_ch06_json from '../../content/quizzes/InstrumentProcedures/ch06.json';
import content_quizzes_InstrumentProcedures_ch07_json from '../../content/quizzes/InstrumentProcedures/ch07.json';
import content_quizzes_InstrumentProcedures_ch08_json from '../../content/quizzes/InstrumentProcedures/ch08.json';
import content_quizzes_PHAK_ch01_json from '../../content/quizzes/PHAK/ch01.json';
import content_quizzes_PHAK_ch02_json from '../../content/quizzes/PHAK/ch02.json';
import content_quizzes_PHAK_ch03_json from '../../content/quizzes/PHAK/ch03.json';
import content_quizzes_PHAK_ch04_json from '../../content/quizzes/PHAK/ch04.json';
import content_quizzes_PHAK_ch05_json from '../../content/quizzes/PHAK/ch05.json';
import content_quizzes_PHAK_ch06_json from '../../content/quizzes/PHAK/ch06.json';
import content_quizzes_PHAK_ch07_json from '../../content/quizzes/PHAK/ch07.json';
import content_quizzes_PHAK_ch08_json from '../../content/quizzes/PHAK/ch08.json';
import content_quizzes_PHAK_ch09_json from '../../content/quizzes/PHAK/ch09.json';
import content_quizzes_PHAK_ch10_json from '../../content/quizzes/PHAK/ch10.json';
import content_quizzes_PHAK_ch11_json from '../../content/quizzes/PHAK/ch11.json';
import content_quizzes_PHAK_ch12_json from '../../content/quizzes/PHAK/ch12.json';
import content_quizzes_PHAK_ch13_json from '../../content/quizzes/PHAK/ch13.json';
import content_quizzes_PHAK_ch14_json from '../../content/quizzes/PHAK/ch14.json';
import content_quizzes_PHAK_ch15_json from '../../content/quizzes/PHAK/ch15.json';
import content_quizzes_PHAK_ch16_json from '../../content/quizzes/PHAK/ch16.json';
import content_quizzes_PHAK_ch17_json from '../../content/quizzes/PHAK/ch17.json';
import content_quizzes_RiskManagement_ch01_json from '../../content/quizzes/RiskManagement/ch01.json';
import content_quizzes_RiskManagement_ch02_json from '../../content/quizzes/RiskManagement/ch02.json';
import content_quizzes_RiskManagement_ch03_json from '../../content/quizzes/RiskManagement/ch03.json';
import content_quizzes_RiskManagement_ch04_json from '../../content/quizzes/RiskManagement/ch04.json';
import content_quizzes_RiskManagement_ch05_json from '../../content/quizzes/RiskManagement/ch05.json';
import content_quizzes_RiskManagement_ch06_json from '../../content/quizzes/RiskManagement/ch06.json';
import content_quizzes_RiskManagement_ch07_json from '../../content/quizzes/RiskManagement/ch07.json';
import content_quizzes_RiskManagement_ch08_json from '../../content/quizzes/RiskManagement/ch08.json';
import content_quizzes_Weather_ch01_json from '../../content/quizzes/Weather/ch01.json';
import content_quizzes_Weather_ch02_json from '../../content/quizzes/Weather/ch02.json';
import content_quizzes_Weather_ch03_json from '../../content/quizzes/Weather/ch03.json';
import content_quizzes_Weather_ch04_json from '../../content/quizzes/Weather/ch04.json';
import content_quizzes_Weather_ch05_json from '../../content/quizzes/Weather/ch05.json';
import content_quizzes_Weather_ch06_json from '../../content/quizzes/Weather/ch06.json';
import content_quizzes_Weather_ch07_json from '../../content/quizzes/Weather/ch07.json';
import content_quizzes_Weather_ch08_json from '../../content/quizzes/Weather/ch08.json';
import content_quizzes_Weather_ch09_json from '../../content/quizzes/Weather/ch09.json';
import content_quizzes_Weather_ch10_json from '../../content/quizzes/Weather/ch10.json';
import content_quizzes_Weather_ch11_json from '../../content/quizzes/Weather/ch11.json';
import content_quizzes_Weather_ch12_json from '../../content/quizzes/Weather/ch12.json';
import content_quizzes_Weather_ch13_json from '../../content/quizzes/Weather/ch13.json';
import content_quizzes_Weather_ch14_json from '../../content/quizzes/Weather/ch14.json';
import content_quizzes_Weather_ch15_json from '../../content/quizzes/Weather/ch15.json';
import content_quizzes_Weather_ch16_json from '../../content/quizzes/Weather/ch16.json';
import content_quizzes_Weather_ch17_json from '../../content/quizzes/Weather/ch17.json';
import content_quizzes_Weather_ch18_json from '../../content/quizzes/Weather/ch18.json';
import content_quizzes_Weather_ch19_json from '../../content/quizzes/Weather/ch19.json';
import content_quizzes_Weather_ch20_json from '../../content/quizzes/Weather/ch20.json';
import content_quizzes_Weather_ch21_json from '../../content/quizzes/Weather/ch21.json';
import content_quizzes_Weather_ch22_json from '../../content/quizzes/Weather/ch22.json';
import content_quizzes_Weather_ch23_json from '../../content/quizzes/Weather/ch23.json';
import content_quizzes_Weather_ch24_json from '../../content/quizzes/Weather/ch24.json';
import content_quizzes_Weather_ch25_json from '../../content/quizzes/Weather/ch25.json';
import content_quizzes_Weather_ch26_json from '../../content/quizzes/Weather/ch26.json';
import content_quizzes_Weather_ch27_json from '../../content/quizzes/Weather/ch27.json';
import content_quizzes_Weather_ch28_json from '../../content/quizzes/Weather/ch28.json';
import content_quizzes_WeightBalance_ch01_json from '../../content/quizzes/WeightBalance/ch01.json';
import content_quizzes_WeightBalance_ch02_json from '../../content/quizzes/WeightBalance/ch02.json';
import content_quizzes_WeightBalance_ch03_json from '../../content/quizzes/WeightBalance/ch03.json';
import content_quizzes_WeightBalance_ch04_json from '../../content/quizzes/WeightBalance/ch04.json';
import content_quizzes_WeightBalance_ch05_json from '../../content/quizzes/WeightBalance/ch05.json';
import content_quizzes_WeightBalance_ch06_json from '../../content/quizzes/WeightBalance/ch06.json';
import content_quizzes_WeightBalance_ch07_json from '../../content/quizzes/WeightBalance/ch07.json';
import content_quizzes_WeightBalance_ch08_json from '../../content/quizzes/WeightBalance/ch08.json';
import content_quizzes_WeightBalance_ch09_json from '../../content/quizzes/WeightBalance/ch09.json';
import content_quizzes_WeightBalance_ch10_json from '../../content/quizzes/WeightBalance/ch10.json';
import content_quizzes_easa_air_law_json from '../../content/quizzes/easa/air-law.json';
import content_quizzes_easa_aircraft_general_knowledge_json from '../../content/quizzes/easa/aircraft-general-knowledge.json';
import content_quizzes_easa_flight_performance_and_planning_json from '../../content/quizzes/easa/flight-performance-and-planning.json';
import content_quizzes_easa_human_performance_and_limitations_json from '../../content/quizzes/easa/human-performance-and-limitations.json';
import content_quizzes_easa_meteorology_json from '../../content/quizzes/easa/meteorology.json';
import content_quizzes_easa_navigation_json from '../../content/quizzes/easa/navigation.json';
import content_quizzes_easa_operational_procedures_json from '../../content/quizzes/easa/operational-procedures.json';
import content_quizzes_easa_principles_of_flight_json from '../../content/quizzes/easa/principles-of-flight.json';
import content_quizzes_easa_vfr_communications_json from '../../content/quizzes/easa/vfr-communications.json';
import content_quizzes_ppl_aerodynamics_json from '../../content/quizzes/ppl/aerodynamics.json';

const allQuizQuestions = [
  ...(content_quizzes_AFH_ch01_json ?? []),
  ...(content_quizzes_AFH_ch02_json ?? []),
  ...(content_quizzes_AFH_ch03_json ?? []),
  ...(content_quizzes_AFH_ch04_json ?? []),
  ...(content_quizzes_AFH_ch05_json ?? []),
  ...(content_quizzes_AFH_ch06_json ?? []),
  ...(content_quizzes_AFH_ch07_json ?? []),
  ...(content_quizzes_AFH_ch08_json ?? []),
  ...(content_quizzes_AFH_ch09_json ?? []),
  ...(content_quizzes_AFH_ch10_json ?? []),
  ...(content_quizzes_AFH_ch11_json ?? []),
  ...(content_quizzes_AFH_ch12_json ?? []),
  ...(content_quizzes_AFH_ch13_json ?? []),
  ...(content_quizzes_AFH_ch14_json ?? []),
  ...(content_quizzes_AFH_ch15_json ?? []),
  ...(content_quizzes_AFH_ch16_json ?? []),
  ...(content_quizzes_AFH_ch17_json ?? []),
  ...(content_quizzes_AFH_ch18_json ?? []),
  ...(content_quizzes_Instrument_ch01_json ?? []),
  ...(content_quizzes_Instrument_ch02_json ?? []),
  ...(content_quizzes_Instrument_ch03_json ?? []),
  ...(content_quizzes_Instrument_ch04_json ?? []),
  ...(content_quizzes_Instrument_ch05_json ?? []),
  ...(content_quizzes_Instrument_ch06_json ?? []),
  ...(content_quizzes_Instrument_ch07_json ?? []),
  ...(content_quizzes_Instrument_ch08_json ?? []),
  ...(content_quizzes_Instrument_ch09_json ?? []),
  ...(content_quizzes_Instrument_ch10_json ?? []),
  ...(content_quizzes_Instrument_ch11_json ?? []),
  ...(content_quizzes_InstrumentProcedures_ch01_json ?? []),
  ...(content_quizzes_InstrumentProcedures_ch02_json ?? []),
  ...(content_quizzes_InstrumentProcedures_ch03_json ?? []),
  ...(content_quizzes_InstrumentProcedures_ch04_json ?? []),
  ...(content_quizzes_InstrumentProcedures_ch05_json ?? []),
  ...(content_quizzes_InstrumentProcedures_ch06_json ?? []),
  ...(content_quizzes_InstrumentProcedures_ch07_json ?? []),
  ...(content_quizzes_InstrumentProcedures_ch08_json ?? []),
  ...(content_quizzes_PHAK_ch01_json ?? []),
  ...(content_quizzes_PHAK_ch02_json ?? []),
  ...(content_quizzes_PHAK_ch03_json ?? []),
  ...(content_quizzes_PHAK_ch04_json ?? []),
  ...(content_quizzes_PHAK_ch05_json ?? []),
  ...(content_quizzes_PHAK_ch06_json ?? []),
  ...(content_quizzes_PHAK_ch07_json ?? []),
  ...(content_quizzes_PHAK_ch08_json ?? []),
  ...(content_quizzes_PHAK_ch09_json ?? []),
  ...(content_quizzes_PHAK_ch10_json ?? []),
  ...(content_quizzes_PHAK_ch11_json ?? []),
  ...(content_quizzes_PHAK_ch12_json ?? []),
  ...(content_quizzes_PHAK_ch13_json ?? []),
  ...(content_quizzes_PHAK_ch14_json ?? []),
  ...(content_quizzes_PHAK_ch15_json ?? []),
  ...(content_quizzes_PHAK_ch16_json ?? []),
  ...(content_quizzes_PHAK_ch17_json ?? []),
  ...(content_quizzes_RiskManagement_ch01_json ?? []),
  ...(content_quizzes_RiskManagement_ch02_json ?? []),
  ...(content_quizzes_RiskManagement_ch03_json ?? []),
  ...(content_quizzes_RiskManagement_ch04_json ?? []),
  ...(content_quizzes_RiskManagement_ch05_json ?? []),
  ...(content_quizzes_RiskManagement_ch06_json ?? []),
  ...(content_quizzes_RiskManagement_ch07_json ?? []),
  ...(content_quizzes_RiskManagement_ch08_json ?? []),
  ...(content_quizzes_Weather_ch01_json ?? []),
  ...(content_quizzes_Weather_ch02_json ?? []),
  ...(content_quizzes_Weather_ch03_json ?? []),
  ...(content_quizzes_Weather_ch04_json ?? []),
  ...(content_quizzes_Weather_ch05_json ?? []),
  ...(content_quizzes_Weather_ch06_json ?? []),
  ...(content_quizzes_Weather_ch07_json ?? []),
  ...(content_quizzes_Weather_ch08_json ?? []),
  ...(content_quizzes_Weather_ch09_json ?? []),
  ...(content_quizzes_Weather_ch10_json ?? []),
  ...(content_quizzes_Weather_ch11_json ?? []),
  ...(content_quizzes_Weather_ch12_json ?? []),
  ...(content_quizzes_Weather_ch13_json ?? []),
  ...(content_quizzes_Weather_ch14_json ?? []),
  ...(content_quizzes_Weather_ch15_json ?? []),
  ...(content_quizzes_Weather_ch16_json ?? []),
  ...(content_quizzes_Weather_ch17_json ?? []),
  ...(content_quizzes_Weather_ch18_json ?? []),
  ...(content_quizzes_Weather_ch19_json ?? []),
  ...(content_quizzes_Weather_ch20_json ?? []),
  ...(content_quizzes_Weather_ch21_json ?? []),
  ...(content_quizzes_Weather_ch22_json ?? []),
  ...(content_quizzes_Weather_ch23_json ?? []),
  ...(content_quizzes_Weather_ch24_json ?? []),
  ...(content_quizzes_Weather_ch25_json ?? []),
  ...(content_quizzes_Weather_ch26_json ?? []),
  ...(content_quizzes_Weather_ch27_json ?? []),
  ...(content_quizzes_Weather_ch28_json ?? []),
  ...(content_quizzes_WeightBalance_ch01_json ?? []),
  ...(content_quizzes_WeightBalance_ch02_json ?? []),
  ...(content_quizzes_WeightBalance_ch03_json ?? []),
  ...(content_quizzes_WeightBalance_ch04_json ?? []),
  ...(content_quizzes_WeightBalance_ch05_json ?? []),
  ...(content_quizzes_WeightBalance_ch06_json ?? []),
  ...(content_quizzes_WeightBalance_ch07_json ?? []),
  ...(content_quizzes_WeightBalance_ch08_json ?? []),
  ...(content_quizzes_WeightBalance_ch09_json ?? []),
  ...(content_quizzes_WeightBalance_ch10_json ?? []),
  ...(content_quizzes_easa_air_law_json ?? []),
  ...(content_quizzes_easa_aircraft_general_knowledge_json ?? []),
  ...(content_quizzes_easa_flight_performance_and_planning_json ?? []),
  ...(content_quizzes_easa_human_performance_and_limitations_json ?? []),
  ...(content_quizzes_easa_meteorology_json ?? []),
  ...(content_quizzes_easa_navigation_json ?? []),
  ...(content_quizzes_easa_operational_procedures_json ?? []),
  ...(content_quizzes_easa_principles_of_flight_json ?? []),
  ...(content_quizzes_easa_vfr_communications_json ?? []),
  ...(content_quizzes_ppl_aerodynamics_json ?? []),
].flat() as ExamQuestion[];

export const faaQuizQuestions = allQuizQuestions.filter((question) => !question.id?.startsWith("easa-"));
export const easaQuizQuestions = allQuizQuestions.filter((question) => question.id?.startsWith("easa-"));
export const fallbackQuizQuestions = allQuizQuestions.filter((question) => question.id?.includes("aerodynamics") || question.id?.includes("ppl"));
